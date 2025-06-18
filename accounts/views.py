from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
import uuid
from .forms import CustomUserCreationForm, CustomAuthenticationForm, SetPasswordForm
from .models import CustomUser


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = (
                False  # User won't be able to login until email is verified
            )
            user.save()

            # Generate verification token
            token = str(uuid.uuid4())
            user.verification_token = token
            user.save()

            # Send verification email
            verification_url = request.build_absolute_uri(
                reverse("accounts:verify_email", kwargs={"token": token})
            )
            send_mail(
                "Verify your email",
                f"Please click this link to verify your email: {verification_url}",
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )

            messages.success(
                request,
                "Registration successful. Please check your email to verify your account.",
            )
            return redirect("accounts:login")
    else:
        form = CustomUserCreationForm()
    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=email, password=password)
            if user is not None:
                if user.is_verified:
                    login(request, user)
                    if not user.has_set_password:
                        return redirect("accounts:set_password")
                    return redirect("admin_dashboard:dashboard")
                else:
                    messages.error(request, "Please verify your email first.")
            else:
                messages.error(request, "Invalid email or password.")
    else:
        form = CustomAuthenticationForm()
    return render(request, "accounts/login.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("index")


def verify_email(request, token):
    try:
        user = CustomUser.objects.get(verification_token=token)
        if not user.is_verified:
            user.is_verified = True
            user.is_active = True
            user.date_verified = timezone.now()
            user.save()
            messages.success(request, "Email verified successfully. You can now login.")
        else:
            messages.info(request, "Email was already verified.")
        return redirect("accounts:login")
    except CustomUser.DoesNotExist:
        messages.error(request, "Invalid verification token.")
        return redirect("index")


@login_required
def set_password(request):
    if request.method == "POST":
        form = SetPasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data["password1"]
            request.user.set_password(password)
            request.user.has_set_password = True
            request.user.save()
            # Re-authenticate the user with new password
            user = authenticate(username=request.user.email, password=password)
            if user:
                login(request, user)
            messages.success(request, "Password set successfully.")
            return redirect("admin_dashboard:dashboard")
    else:
        form = SetPasswordForm()
    return render(request, "accounts/set_password.html", {"form": form})
