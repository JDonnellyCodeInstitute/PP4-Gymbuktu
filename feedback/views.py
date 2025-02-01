from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Feedback
from .forms import FeedbackForm

@login_required
def feedback_view(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            return redirect("feedback_received")
    else:
        form = FeedbackForm()

    feedback_entries = Feedback.objects.filter(user=request.user).order_by("-timestamp")

    return render(request, "feedback/feedback_form.html", {"form": form, "feedback_entries": feedback_entries})