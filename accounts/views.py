from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth import login

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login') # Redirecting to login page once registered

    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form}) # Returns sign up template