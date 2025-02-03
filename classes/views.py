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
    
    # Check if user has already booked class
    existing_booking = Booking.objects.filter(user=request.user, gym_class=gym_class, class_status=0).exists()
    
    if existing_booking:
        return render(request, "classes/booking_confirmation.html", {
            "gym_class": gym_class,
            "error": "You have already booked this class."
        })
    # Confirm there is a space available in the class
    if gym_class.available_slots() <= 0:
        return render(request, "classes/booking_confirmation.html", {
            "gym_class": gym_class,
            "error": "No available slots."
        })
    
    if request.method == "POST":
        Booking.objects.create(user=request.user, gym_class=gym_class)
        return redirect("booking_confirmation", class_id=gym_class.id)
    
    return render(request, "classes/booking_confirmation.html", {"gym_class": gym_class})

def booking_confirmation(request, class_id):
    gym_class = get_object_or_404(Class, id=class_id)
    return render(request, "classes/booking_confirmation.html", {"gym_class": gym_class})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == "POST":
        booking.class_status = 1
        booking.save()
        return redirect("class_list")

    return render(request, "classes/cancel_booking.html", {"booking": booking})