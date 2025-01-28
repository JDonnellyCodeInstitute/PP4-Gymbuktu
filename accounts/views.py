from django.shortcuts import render, redirect
from .forms import SignUpForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('') # Redirecting to the homepage for now until the login page is implemented

    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form}) # Returns sign up template