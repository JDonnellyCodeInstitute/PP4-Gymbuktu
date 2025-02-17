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

  Testing: Core functionalities (e.g., user management, booking, and admin tools) will undergo a mix of automated and manual testing.

  Deployment: The system will be deployed on the cloud platform Heroku for accessibility and scalability.

6. Success Metrics

  The project will be deemed successful if:

  - Gym members can register, log in, and book classes without errors.
  - Administrators can efficiently manage class schedules and bookings.
  - The system provides a responsive, mobile-friendly user experience.

## The Five Planes of User Experience

### **The Strategy Plane**
#### **Defining Goals and User Needs:**
- The goal of GymBukTu is to provide a user-friendly gym booking system that allows gym members to book, manage, and cancel classes while offering gym administrators tools to manage schedules and attendance.
- The system should provide a smooth and intuitive booking process, ensuring users can quickly find available classes and receive on-screen confirmations.
- Members need an efficient way to track their upcoming and past bookings, which is achieved through the profile page.
- Admins should have an easy-to-use interface for class management, ensuring they can update schedules and manage attendance without hassle.
- The system follows an **Agile development process**.

### **The Scope Plane**
#### **Determining Features and Content:**
- **Core Features:**
  - User authentication (sign-up, login, logout).
  - Booking system allowing members to book, manage, and cancel classes.
  - Gym administrators can add, edit, and remove classes.
  - Mobile-friendly design for non-admin users for easy access on various devices.
  
- **Additional Features (Should-Haves & Nice-To-Haves):**
  - A waitlist system for fully booked classes.
  - Class reminders and notifications to reduce no-shows.
  - A feedback system allowing users to rate classes.
  - A progressive web app (PWA) for an app-like experience.
  
### **The Structure Plane**
#### **Setting the Sitemap and Logical Flow:**
- The system follows a clear and structured navigation flow, ensuring users can access the most critical features with minimal effort.
- The primary navigation links include:
  - **Home** – Landing page including hero image, sign up link and testimonials.
  - **Classes** – List of available gym classes with booking options.
  - **Profile** – Displays current and past bookings with management options.
  - **Feedback** – Users can submit general feedback.
  - **Manage Classes** - Only available to staff, this is the frontend where staff can create, update and delete classes.

### **The Skeleton Plane**
#### **Layout and Navigation Design:**
- **Mobile-First Approach:**
  - Navigation uses a burger menu for compact mobile usability.
  - Responsive design ensures smooth user experience across devices.
  - Only exception is the manage classes section where it would be expected that staff with CRUD functionality can only access the system via an onsite computer, not on their personal devices.
- **User Flow Considerations:**
  - Bookings appear first on the profile page, with past bookings listed below.
  - Successful feedback submission redirects users to a thank-you page for confirmation.
  - Error handling and validation messages guide users if they input incorrect data.

### **The Surface Plane**
#### **Visual Design and Styling:**
- The interface follows a minimalist design, ensuring users can focus on the core functionalities without distractions.
- Bootstrap is used to provide a clean, professional look while maintaining simplicity.
- Consistent color schemes enhance the user experience:
  - Green for success messages (e.g., booking confirmation).
  - Red for errors and cancellations.
  - Blue for informational messages.
- Simple and readable typography ensures accessibility and ease of use.
- Icons are used sparingly to indicate actions (e.g., edit, delete, view details).

---
This structured approach ensures GymBukTu provides a smooth and efficient user experience while maintaining clarity and ease of use for both gym members and administrators.

## Wireframes

The wireframes are reflective of the simple theme of the site's styling, generally, bootstrap, and in particular the bootstrap card class, is used to present information clearly and efficiently, usually acting to signpost or navigate the user as required. Below we'll highlight where more was planned and implemented than the simple bootstrap card.

The first schematic was a simple one for the hypothetical layout of gymbuktu showing the reception area and the two main facilities referred to in most classes.

![LAYOUT](static\images\readme\wireframes\layout.png)

The **home page** changed little in the translation from wire frame bar the spacing of the testimonials on the smaller screen. It was felt that bootstrap's simple block spacing made for a sleeker look. The non-social media section of the footer is also hidden on smaller screens to avoid clutter.

![HOME](static\images\readme\wireframes\home-page.png)

The **classes page** is majoritively the same as the wireframes also, with slight formatting changes on smaller screens.

![CLASSES](static\images\readme\wireframes\classes.png)

The **class_detail** page changed more significantly than most with the addition of a second card to house status information and the booking / cancellation buttons.

![DETAIL](static\images\readme\wireframes\class-detail.png)

The **manage classes** page is close to the below with some updates to formatting and an added button for staff to manage classes manually.

![MANAGE](static\images\readme\wireframes\manage-classes.png)

The **profile page** was altered to have the quick links section appear more cleanly at the bottom of the information presented.

![PROFILE](static\images\readme\wireframes\profile.png)

The **feedback page** again is basically as planned but during development functionality was added to allow users to see their submitted input beneath the form.

![FEEDBACK](static\images\readme\wireframes\feedback.png)

The gym rules page and additional / connection pages are all laid out roughly the same with a bootstrap card as the focal point. The same is true of the rest of the informational pages mainly stored in the accounts and classes apps such as password reset complete, already verified, booking confirmation, cancel booking, etc.

![GENERIC](static\images\readme\wireframes\generic.png)

## ERD

ERD for database connectivity as per below. Note: The maximum capacity in the class model is limited to the capacity of the facility the class is being held in.

![SCHEMA](static\images\readme\erd\erd-schema.png)
![ERD](static\images\readme\erd\ERD.png)

## PEP8 Compliance

PEP8 compliance for each app is confirmed below excluding migration and venv code, and the env import in settings.py for hosting the server in development.

![ALL](static\images\readme\pep8\pep8-all.png)