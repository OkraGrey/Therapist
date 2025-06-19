from django.urls import path
from . import views

app_name = "forms"

urlpatterns = [
    path("create/", views.create_form, name="create_form"),
    path("<int:form_id>/", views.public_form_view, name="public_form"),
    path("<int:form_id>/success/", views.submission_success, name="submission_success"),
    path("<int:form_id>/edit/", views.edit_form, name="edit_form"),
    path("<int:form_id>/delete/", views.delete_form, name="delete_form"),
]
