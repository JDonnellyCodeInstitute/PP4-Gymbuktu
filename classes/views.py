from django.shortcuts import render, get_object_or_404, redirect
from .models import Class, Booking, Instructor
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.exceptions import ValidationError
import datetime


def class_list(request):
    """Display all upcoming classes with optional filters."""
    # Current time
    now = timezone.now()
    today = now.date()
    tomorrow = today + datetime.timedelta(days=1)

    # Base querysets
    classes = Class.objects.filter(start_time__date=today)
    instructors = Instructor.objects.all()

    # Get query parameters
    class_type = request.GET.get("class_type", "").strip()
    date_filter = request.GET.get("date", "").strip()
    instructor_id = request.GET.get("instructor", "").strip()

    # Apply filters
    # Convert date_filter to valid date format
    selected_date = today  # Default to today
    formatted_date = "Today"  # Default display

    if date_filter:
        try:
            selected_date = datetime.datetime.strptime(
                date_filter, "%Y-%m-%d").date()
            if selected_date == today:
                formatted_date = "Today"
            elif selected_date == tomorrow:
                formatted_date = "Tomorrow"
            else:
                formatted_date = selected_date.strftime("%A, %d %B %Y")
            classes = Class.objects.filter(start_time__date=selected_date)
        except ValueError:
            selected_date = today
            formatted_date = "Today"

    if class_type:
        classes = classes.filter(name__icontains=class_type)

    if date_filter:
        classes = classes.filter(start_time__date=date_filter)

    if instructor_id:
        classes = classes.filter(instructor_id=instructor_id)

    return render(request, "classes/class_list.html", {
        "classes": classes,
        "instructors": instructors,
        "now": now,
        "selected_date": selected_date,
        "formatted_date": formatted_date,
    })


def class_detail(request, class_id):
    gym_class = get_object_or_404(Class, id=class_id)
    now = timezone.now()

    # Get the user's booking (if any)
    booking = None
    if request.user.is_authenticated:
        booking = Booking.objects.filter(
            user=request.user, gym_class=gym_class, class_status=0).first()

    return render(request, "classes/class_detail.html", {
        "gym_class": gym_class,
        "has_booking": booking is not None,
        "booking_id": booking.id if booking else None,
        "now": now
    })


@login_required
def book_class(request, class_id):
    gym_class = get_object_or_404(Class, id=class_id)

    # Check if user has already booked class
    existing_booking = Booking.objects.filter(
        user=request.user, gym_class=gym_class, class_status=0).exists()

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
        try:
            # Try creating a new booking
            booking = Booking(user=request.user, gym_class=gym_class)
            booking.full_clean()  # Runs model validations before saving
            booking.save()
            return redirect("booking_confirmation", class_id=gym_class.id)

        except ValidationError as e:
            return render(request, "classes/booking_confirmation.html", {
                "gym_class": gym_class,
                "error": e.messages[0]  # Extracts error message
            })

    return render(request, "classes/booking_confirmation.html",
                  {"gym_class": gym_class})


@login_required
def booking_confirmation(request, class_id):
    gym_class = get_object_or_404(Class, id=class_id)
    return render(request, "classes/booking_confirmation.html",
                  {"gym_class": gym_class})


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == "POST":
        booking.class_status = 1
        booking.save()
        return redirect("class_list")

    return render(request, "classes/cancel_booking.html", {"booking": booking})
