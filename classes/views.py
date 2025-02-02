from django.shortcuts import render, get_object_or_404, redirect
from .models import Class, Booking
from django.contrib.auth.decorators import login_required

def class_list(request):
    classes = Class.objects.all()
    return render(request, "classes/class_list.html", {"classes": classes})

def class_detail(request, class_id):
    gym_class = get_object_or_404(Class, id=class_id)
    return render(request, "classes/class_detail.html", {"gym_class": gym_class})

@login_required
def book_class(request, class_id):
    gym_class = get_object_or_404(Class, id=class_id)
    
    if gym_class.available_slots() <= 0:
        return render(request, "classes/booking_confirmation.html", {"gym_class": gym_class, "error": "No available slots."})
    
    if request.method == "POST":
        Booking.objects.create(user=request.user, gym_class=gym_class)
        gym_class.booked_slots += 1
        gym_class.save()
        return redirect("booking_confirmation", class_id=gym_class.id)
    
    return render(request, "classes/booking_confirmation.html", {"gym_class": gym_class})