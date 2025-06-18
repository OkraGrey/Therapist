from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import Form, Question, ChoiceOption

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
