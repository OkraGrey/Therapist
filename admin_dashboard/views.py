from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from forms.models import Form, Submission

# Create your views here.


@login_required
def dashboard(request):
    forms = Form.objects.all().order_by("-created_at")
    return render(request, "admin_dashboard/dashboard.html", {"forms": forms})


@login_required
def view_submissions(request, form_id):
    """View all submissions for a specific form"""
    form = get_object_or_404(Form, id=form_id)
    submissions = form.submissions.all().order_by("-submitted_at").prefetch_related("answers__question", "answers__choice_answer")
    email_submissions_count = submissions.exclude(email__isnull=True).exclude(email="").count()
    
    context = {
        "form": form,
        "submissions": submissions,
        "email_submissions_count": email_submissions_count,
    }
    return render(request, "admin_dashboard/submissions.html", context)
