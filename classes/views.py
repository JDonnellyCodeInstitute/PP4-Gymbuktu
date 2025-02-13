from django.shortcuts import render, get_object_or_404, redirect
from .models import Class, Booking, Instructor, User
from .forms import ClassForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib import messages
import datetime
from django.contrib.auth.decorators import user_passes_test
from django.core.mail import send_mail
from django.conf import settings

# Staff specific views


def staff_required(user):
    """Restrict view access to staff and superusers."""
    return user.is_staff or user.is_superuser


@user_passes_test(staff_required)
def manage_classes(request):
    """Show all classes and allow staff to add/edit/delete."""
    today = timezone.now().date()
    selected_date = request.GET.get("date")

    # Default to today if no date provided
    if not selected_date:
        selected_date = today
    else:
        # Ensure date is properly formatted
        try:
            selected_date = timezone.datetime.strptime(
                selected_date, "%Y-%m-%d"
            ).date()
        except ValueError:
            selected_date = today  # Default to today if invalid

    classes = Class.objects.filter(start_time__date=selected_date)

    return render(request, "classes/manage_classes.html", {
        "classes": classes,
        "selected_date": selected_date,
    })


@user_passes_test(staff_required)
def manage_attendance(request, class_id):
    """Allow staff to view and mark attendance for a class."""
    gym_class = get_object_or_404(Class, id=class_id)
    bookings = Booking.objects.filter(gym_class=gym_class, class_status=0)

    if request.method == "POST":
        attendees = []
        for booking in bookings:
            attended = request.POST.get(f"attended_{booking.id}") == "on"
            booking.attended = attended
            booking.save()

            if attended:
                attendees.append(booking.user)

        # Update the class's attendees list
        gym_class.attendees.set(attendees)

        messages.success(request, "Attendance updated successfully!")
        return redirect("manage_classes")

    return render(request, "classes/manage_attendance.html", {
        "gym_class": gym_class,
        "bookings": bookings
    })


@user_passes_test(staff_required)
def add_class(request):
    """Allow staff to add a new class."""
    if request.method == "POST":
        form = ClassForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Class added successfully!")
            return redirect("manage_classes")
    else:
        form = ClassForm()

    return render(request, "classes/class_form.html", {
        "form": form, "title": "Add Class"})


@user_passes_test(staff_required)
def edit_class(request, class_id):
    """Allow staff to edit an existing class."""
    gym_class = get_object_or_404(Class, id=class_id)
    if request.method == "POST":
        form = ClassForm(request.POST, instance=gym_class)
        if form.is_valid():
            form.save()
            messages.success(request, "Class updated successfully!")
            return redirect("manage_classes")
    else:
        form = ClassForm(instance=gym_class)

    return render(request, "classes/class_form.html", {
        "form": form, "title": "Edit Class"})


@user_passes_test(staff_required)
def delete_class(request, class_id):
    """Allow staff to delete a class and notify users with bookings."""
    gym_class = get_object_or_404(Class, id=class_id)

    # Fetch users who have booked this class
    booked_users = User.objects.filter(
        booking__gym_class=gym_class, booking__class_status=0).distinct()

    if request.method == "POST":
        # Send email notifications before deleting the class
        subject = f"GymBukTu Class Cancellation: {gym_class.name}"
        message = (
            f"Dear Member,\n\n"
            f"Regretfully, your booked class '{gym_class.name}' on "
            f"{gym_class.start_time.strftime('%A, %d %B %Y at %H:%M')} "
            f"has been cancelled.\n\n"
            f"We apologize for any inconvenience caused.\n\n"
            f"Best regards,\nThe GymBukTu Team"
        )

        recipient_list = [user.email for user in booked_users if user.email]

        if recipient_list:
            send_mail(
                subject, message,
                settings.DEFAULT_FROM_EMAIL,
                recipient_list
            )

        # Delete the class
        gym_class.delete()

        messages.success(
            request,
            "Class deleted successfully! Affected members have been notified."
        )
        return redirect("manage_classes")

    return render(
        request, "classes/confirm_delete.html", {"gym_class": gym_class})

# User centric views


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


@login_required
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
        booking.class_status = 1  # Set status to Cancelled
        booking.save()

        messages.success(request, "Booking successfully canceled.")

        # Redirect based on where the user came from
        if "profile" in request.META.get("HTTP_REFERER", ""):
            return redirect("profile")  # Send user back to profile
        else:
            return redirect("class_list")  # Default to class list

    return render(request, "classes/cancel_booking.html", {"booking": booking})
