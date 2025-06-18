from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    """
    Landing page view for The Therapist application.
    """
    return render(request, "index.html")
