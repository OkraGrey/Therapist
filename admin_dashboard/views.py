from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from forms.models import Form

# Create your views here.


@login_required
def dashboard(request):
    forms = Form.objects.all().order_by("-created_at")
    return render(request, "admin_dashboard/dashboard.html", {"forms": forms})
