from django.urls import path
from . import views

app_name = "admin_dashboard"

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("forms/<int:form_id>/submissions/", views.view_submissions, name="view_submissions"),
]
