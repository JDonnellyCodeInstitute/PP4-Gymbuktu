from django import forms
from .models import Class


class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ["name", "description", "instructor",
                  "facility", "start_time", "end_time",
                  "repeat_schedule"]
        widgets = {
            "start_time": forms.DateTimeInput(attrs={
                "type": "datetime-local"}),
            "end_time": forms.DateTimeInput(attrs={
                "type": "datetime-local"}),
        }
