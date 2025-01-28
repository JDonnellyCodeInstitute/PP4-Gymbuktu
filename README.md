# Gymbuktu

## Project Scope

1. Purpose

  The purpose of this project is to develop a gym booking system that enables gym members to book, manage, and cancel classes conveniently. It will also provide gym administrators with tools to manage class schedules and attendance efficiently.

2. Target Audience

    - Primary Users: Gym members seeking a user-friendly platform to book classes, view schedules, and manage their bookings.
    - Secondary Users: Gym administrators or staff responsible for overseeing class management and attendance.

3. Scope of Features

  - 3.1 Minimum Viable Product (MVP)

  The following features are essential for the system:

  - User Management:

    - Member registration and login functionality with email verification.
    - Secure user authentication leveraging Django’s built-in features.

  - Booking System:

    - Browse and search for available gym classes.
    - Book a class with available slots.
    - Cancel bookings.
    - View personal booking history.

  - Class Management:

    - Admin functionality to add, edit, and delete gym classes.
    - Admin tools to manage class bookings and attendance.

  - Schedules:

    - Calendar or list view displaying gym classes for users.

  - 3.2 Nice-to-Have Features

  These features are not critical but will enhance the system’s value if implemented:

  - Waitlists:

    - Allow users to join a waitlist if a class is full.

  - Notifications:

    - Email reminders for upcoming classes.
    - Notifications for changes or cancellations.

  - User Reviews and Ratings:

    - Enable members to rate and review classes or instructors.

  - Mobile-Friendly Enhancements:

    - Develop a Progressive Web App (PWA) for better mobile accessibility.

4. Out of Scope

  The following features will not be included in this project to prevent scope creep:

  - Real-time payment integration.
  - Detailed fitness tracking or health metrics.
  - Multi-gym or franchise-level management capabilities.

5. Technical Constraints

  Frontend: The system’s user interface will use Bootstrap to ensure a responsive and consistent design.

  Backend: The backend will be built using the Django framework for its robust features and scalability.

  Database: PostgreSQL will be used as the relational database for storing and managing data.

  Testing: Core functionalities (e.g., user management, booking, and admin tools) will undergo automated testing.

  Deployment: The system will be deployed on the cloud platform Heroku for accessibility and scalability.

6. Success Metrics

  The project will be deemed successful if:

  - Gym members can register, log in, and book classes without errors.
  - Administrators can efficiently manage class schedules and bookings.
  - The system provides a responsive, mobile-friendly user experience.


Code for later:
Testimonial image src:
{% static 'images/gym-goer-1.jpg' %}
{% static 'images/gym-goer-2.jpg' %}
{% static 'images/gym-goer-3.jpg' %}

NavBar HREFs:
{% url 'classes' %}
{% url 'feedback' %}
{% url 'profile' %}
{% url 'logout' %}
{% url 'login' %}


Footer HREF:
{% url 'rules' %}

Hero banner:
{% url 'signup' %}