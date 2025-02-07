from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUpForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from classes.models import Booking
from django.contrib.auth.models import User
import uuid
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

            # EmailJS Data
            email_data = {
                "to_email": user.email,
                "username": user.username,
                "verification_link": f"http://yourdomain.com/accounts/verify/{token_obj.token}/"
            }

            # Send email
            send_mail(
                "Verify Your Account",
                f"Click the link to verify your account: {email_data['verification_link']}",
                "joe.donnelly.bmc@gmail.com",
                [user.email],
                fail_silently=False,
            )

            return redirect("check_email")  # Redirect to check your email page

    else:
        form = SignUpForm()

    return render(request, 'accounts/signup.html', {'form': form})




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