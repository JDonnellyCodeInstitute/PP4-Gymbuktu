from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm, CustomLoginForm
from classes.models import Booking, User
from django.core.mail import send_mail
from .models import EmailVerification
from django.contrib.auth.password_validation import (
    validate_password,
    get_default_password_validators
)
from django.core.exceptions import ValidationError


def signup(request):
    """Handles user registration and prevents duplicate signups."""
    if request.method == "POST":
        form = SignUpForm(request.POST)
        password = request.POST.get("password1")
        username = request.POST.get("username")

        # Check if a user with this username already exists
        if User.objects.filter(username=username).exists():
            messages.error(
                request,
                "This username is already taken. "
                "Please choose another or log in."
            )
            return render(request, "accounts/signup.html", {"form": form})

        # Check if the password meets Django's password policy
        try:
            validate_password(
                password, user=None,
                password_validators=get_default_password_validators()
            )
        except ValidationError as e:
            messages.error(
                request,
                f"Your password does not meet the security requirements:\n"
                f"{' '.join(e.messages)}"
            )
            return render(request, "accounts/signup.html", {"form": form})

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Prevent login until verification
            user.save()

            # Create verification token
            token_obj = EmailVerification.objects.create(user=user)

            # Get site domain so verification works in prod or dev
            current_site = request.get_host()
            verification_link = (
                f"http://{current_site}/accounts/verify/{token_obj.token}/"
            )

            # Send email
            send_mail(
                "Verify Your Account",
                f"Click to verify your account:\n{verification_link}",
                "gymbuktu@gmail.com",
                [user.email],
                fail_silently=False,
            )

            return redirect("check_email")

    else:
        form = SignUpForm()

    return render(request, "accounts/signup.html", {"form": form})


def login_view(request):
    """Custom login view with verification check and error messages."""
    form = CustomLoginForm(request, data=request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect("profile")

        else:
            messages.error(
                request,
                "Username or password is unrecognised.\n"
                "Username and password will only be recognised once you've "
                "followed the verification link in your email after sign-up."
            )

    return render(request, "accounts/login.html", {"form": form})


def verify_email(request, token):
    """Verifies user's email and activates their account."""
    token_obj = get_object_or_404(EmailVerification, token=token)

    if token_obj.is_verified:
        return render(request, "accounts/already_verified.html")

    # Activate user account
    user = token_obj.user
    user.is_active = True
    user.save()

    token_obj.is_verified = True
    token_obj.save()

    messages.success(
        request, "Your account has been verified. You can now log in."
        )
    return redirect("login")


def check_email(request):
    """Displays a message prompting the user
    to check their email for verification."""
    return render(request, "accounts/check_email.html")


def already_verified(request):
    """Displays a message when a user tries
    to verify an already-verified account."""
    return render(request, "accounts/already_verified.html")


@login_required
def profile(request):
    """Displays the user's profile with their bookings."""
    current_bookings = Booking.objects.filter(
        user=request.user, class_status=0)
    past_bookings = Booking.objects.filter(user=request.user, class_status=2)

    return render(
        request,
        'accounts/profile.html',
        {
            'current_bookings': current_bookings,
            'past_bookings': past_bookings,
        }
    )


def auto_logout(request):
    """Logs out user after inactivity and
    redirects to login page with a message."""
    logout(request)
    messages.warning(request, "You have been logged out due to inactivity.")
    return redirect("login")
