from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm
from classes.models import Booking
from django.core.mail import send_mail
from .models import EmailVerification


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Prevent login until verification
            user.save()

            # Create verification token
            token_obj = EmailVerification.objects.create(user=user)

            # Get site domain so verification works in prod or dev
            current_site = request.get_host()
            verification_link = f"http://{current_site}/accounts/verify/{token_obj.token}/"

            # EmailJS Data
            email_data = {
                "to_email": user.email,
                "username": user.username,
                "verification_link": verification_link
            }

            # Send email
            send_mail(
                "Verify Your Account",
                f"""
                Click to verify your account:
                {email_data['verification_link']}""",
                "joe.donnelly.bmc@gmail.com",
                [user.email],
                fail_silently=False,
            )

            return redirect("check_email")  # Redirect to check your email page

    else:
        form = SignUpForm()

    return render(request, 'accounts/signup.html', {'form': form})


def verify_email(request, token):
    token_obj = get_object_or_404(EmailVerification, token=token)

    if token_obj.is_verified:
        return render(request, "accounts/already_verified.html")

    # Activate user account
    user = token_obj.user
    user.is_active = True
    user.save()

    token_obj.is_verified = True
    token_obj.save()

    return redirect("login")


def check_email(request):
    """Displays a message prompting the user
    to check their email for verification."""
    return render(request, "accounts/check_email.html")


def already_verified(request):
    """Displays a message when a user
    tries to verify an already-verified account."""
    return render(request, "accounts/already_verified.html")


@login_required
def profile(request):
    current_bookings = Booking.objects.filter(user=request.user, class_status=0)
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
    """Logs out user after inactivity and redirects to login page with a message."""
    logout(request)
    messages.warning(request, "You have been logged out due to inactivity.")
    return redirect("login")
