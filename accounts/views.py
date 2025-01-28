from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from classes.models import Booking

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')  # Redirecting to profile after signup

    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})  # Returns sign-up template

@login_required
def profile(request):
    current_bookings = Booking.objects.filter(user=request.user, status="upcoming")
    past_bookings = Booking.objects.filter(user=request.user, status="completed")

    return render(
        request,
        'accounts/profile.html',
        {
            'current_bookings': current_bookings,
            'past_bookings': past_bookings,
        }
    )