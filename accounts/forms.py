from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth import authenticate

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class CustomLoginForm(AuthenticationForm):
    def clean(self):
        cleaned_data = super().clean()
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                if not user.is_active:
                    raise forms.ValidationError("Please verify your email before logging in.")
        
        return cleaned_data
