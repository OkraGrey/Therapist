from django.urls import path
from . import views

app_name = "forms"

urlpatterns = [
    path("create/", views.create_form, name="create_form"),
]
