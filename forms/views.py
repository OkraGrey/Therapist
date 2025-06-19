from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_POST
from .models import Form, Question, ChoiceOption, Submission, Answer

# Create your views here.


@login_required
def create_form(request):
    """Create new forms with questions and choice options"""
    if request.method == "POST":
        try:
            with transaction.atomic():
                # Get form data
                form_name = request.POST.get("name")
                form_description = request.POST.get("description", "")

                # Create the form
                form = Form.objects.create(name=form_name, description=form_description)

                # Process questions
                questions_data = {}
                for key, value in request.POST.items():
                    if key.startswith("questions[") and key.endswith("]"):
                        # Parse the key to extract question index and field
                        parts = key[10:-1].split("][")  # Remove 'questions[' and ']'
                        if len(parts) >= 2:
                            question_index = parts[0]
                            field_name = parts[1]

                            if question_index not in questions_data:
                                questions_data[question_index] = {}

                            if field_name == "choices":
                                if "choices" not in questions_data[question_index]:
                                    questions_data[question_index]["choices"] = []
                                questions_data[question_index]["choices"].append(value)
                            else:
                                questions_data[question_index][field_name] = value

                # Create questions and choice options
                for question_index, question_data in questions_data.items():
                    if "text" in question_data and "type" in question_data:
                        # Create the question
                        question = Question.objects.create(
                            form=form,
                            text=question_data["text"],
                            type=question_data["type"],
                            is_mandatory=question_data.get("is_mandatory") == "on",
                            order=int(question_index),
                        )

                        # Create choice options if it's a choice question
                        if (
                            question_data["type"] == "choice"
                            and "choices" in question_data
                        ):
                            for choice_index, choice_text in enumerate(
                                question_data["choices"]
                            ):
                                if (
                                    choice_text.strip()
                                ):  # Only create if choice text is not empty
                                    ChoiceOption.objects.create(
                                        question=question,
                                        text=choice_text.strip(),
                                        order=choice_index,
                                    )

                messages.success(request, f'Form "{form.name}" created successfully!')
                return redirect("admin_dashboard:dashboard")

        except Exception as e:
            messages.error(request, f"Error creating form: {str(e)}")
            return redirect("forms:create_form")

    return render(request, "forms/create_form.html")


@login_required
def edit_form(request, form_id):
    """Edit existing forms with questions and choice options"""
    form = get_object_or_404(Form, id=form_id)
    
    if request.method == "POST":
        try:
            with transaction.atomic():
                # Update form data
                form.name = request.POST.get("name")
                form.description = request.POST.get("description", "")
                form.save()

                # Delete existing questions and choices
                form.questions.all().delete()

                # Process questions (same logic as create_form)
                questions_data = {}
                for key, value in request.POST.items():
                    if key.startswith("questions[") and key.endswith("]"):
                        parts = key[10:-1].split("][")
                        if len(parts) >= 2:
                            question_index = parts[0]
                            field_name = parts[1]

                            if question_index not in questions_data:
                                questions_data[question_index] = {}

                            if field_name == "choices":
                                if "choices" not in questions_data[question_index]:
                                    questions_data[question_index]["choices"] = []
                                questions_data[question_index]["choices"].append(value)
                            else:
                                questions_data[question_index][field_name] = value

                # Create questions and choice options
                for question_index, question_data in questions_data.items():
                    if "text" in question_data and "type" in question_data:
                        question = Question.objects.create(
                            form=form,
                            text=question_data["text"],
                            type=question_data["type"],
                            is_mandatory=question_data.get("is_mandatory") == "on",
                            order=int(question_index),
                        )

                        if (
                            question_data["type"] == "choice"
                            and "choices" in question_data
                        ):
                            for choice_index, choice_text in enumerate(
                                question_data["choices"]
                            ):
                                if choice_text.strip():
                                    ChoiceOption.objects.create(
                                        question=question,
                                        text=choice_text.strip(),
                                        order=choice_index,
                                    )

                messages.success(request, f'Form "{form.name}" updated successfully!')
                return redirect("admin_dashboard:dashboard")

        except Exception as e:
            messages.error(request, f"Error updating form: {str(e)}")
            return redirect("forms:edit_form", form_id=form_id)

    # Get existing questions for the form
    questions = form.questions.all().prefetch_related("choices")
    
    context = {
        "form": form,
        "questions": questions,
        "is_edit": True,
    }
    return render(request, "forms/create_form.html", context)


@login_required
@require_POST
def delete_form(request, form_id):
    """Delete a form and all its associated data"""
    form = get_object_or_404(Form, id=form_id)
    form_name = form.name
    
    try:
        form.delete()
        messages.success(request, f'Form "{form_name}" deleted successfully!')
    except Exception as e:
        messages.error(request, f"Error deleting form: {str(e)}")
    
    return redirect("admin_dashboard:dashboard")


def public_form_view(request, form_id):
    """Display a specific form for public users and handle submissions"""
    form = get_object_or_404(Form, id=form_id)
    questions = form.questions.all()  # This will get all questions for the form

    # Prefetch choice options for choice questions to optimize database queries
    questions = questions.prefetch_related("choices")

    if request.method == "POST":
        # Handle form submission
        try:
            with transaction.atomic():
                # Get optional email from form
                email = request.POST.get("email", "").strip()
                
                # Create submission
                submission = Submission.objects.create(
                    form=form,
                    email=email if email else None
                )

                # Process answers
                validation_errors = []
                
                for question in questions:
                    answer_key = f"answer_{question.id}"
                    answer_value = request.POST.get(answer_key, "").strip()
                    
                    # Validate mandatory fields
                    if question.is_mandatory and not answer_value:
                        validation_errors.append(f"Question {question.text[:50]}... is required.")
                        continue
                    
                    # Create answer based on question type
                    if question.type == "text":
                        Answer.objects.create(
                            submission=submission,
                            question=question,
                            text_answer=answer_value
                        )
                    elif question.type == "choice":
                        try:
                            choice = ChoiceOption.objects.get(id=answer_value, question=question)
                            Answer.objects.create(
                                submission=submission,
                                question=question,
                                choice_answer=choice
                            )
                        except ChoiceOption.DoesNotExist:
                            if question.is_mandatory:
                                validation_errors.append(f"Please select a valid option for: {question.text[:50]}...")
                    elif question.type == "range":
                        try:
                            range_value = int(answer_value)
                            if 1 <= range_value <= 5:
                                Answer.objects.create(
                                    submission=submission,
                                    question=question,
                                    range_answer=range_value
                                )
                            else:
                                validation_errors.append(f"Please select a valid rating (1-5) for: {question.text[:50]}...")
                        except (ValueError, TypeError):
                            if question.is_mandatory:
                                validation_errors.append(f"Please select a valid rating (1-5) for: {question.text[:50]}...")
                
                # If there are validation errors, rollback and show errors
                if validation_errors:
                    raise ValueError("Validation errors occurred")
                
                # Send confirmation email if email was provided
                if email and hasattr(settings, 'EMAIL_HOST'):
                    try:
                        send_mail(
                            subject=f'Form Submission Confirmation - {form.name}',
                            message=f'''Thank you for submitting your response to "{form.name}".

Your response has been submitted successfully and will be reviewed.

Best regards,
The Therapist Team''',
                            from_email=settings.DEFAULT_FROM_EMAIL or 'noreply@thetherapist.com',
                            recipient_list=[email],
                            fail_silently=True,
                        )
                    except Exception as e:
                        # Log email error but don't fail the submission
                        print(f"Email sending failed: {e}")
                
                # Redirect to success page
                return HttpResponseRedirect(reverse('forms:submission_success', kwargs={'form_id': form_id}))
                
        except ValueError:
            # Validation errors occurred
            for error in validation_errors:
                messages.error(request, error)
        except Exception as e:
            messages.error(request, f"An error occurred while submitting your form. Please try again.")
            print(f"Form submission error: {e}")

    context = {
        "form": form,
        "questions": questions,
    }
    return render(request, "forms/public_form.html", context)


def submission_success(request, form_id):
    """Display submission success page"""
    form = get_object_or_404(Form, id=form_id)
    return render(request, "forms/submission_success.html", {"form": form})
