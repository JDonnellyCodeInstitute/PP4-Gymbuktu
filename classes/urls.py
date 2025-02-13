from django.urls import path
from . import views

urlpatterns = [
    path("", views.class_list, name="class_list"),
    path("<int:class_id>/", views.class_detail, name="class_detail"),
    path("<int:class_id>/book/", views.book_class, name="book_class"),
    path(
        "cancel/<int:booking_id>/",
        views.cancel_booking,
        name="cancel_booking"
    ),
    path(
        "<int:class_id>/confirmation/",
        views.booking_confirmation,
        name="booking_confirmation"
    ),
    path("manage/", views.manage_classes, name="manage_classes"),
    path("manage/add/", views.add_class, name="add_class"),
    path("manage/edit/<int:class_id>/", views.edit_class, name="edit_class"),
    path(
        "manage/delete/<int:class_id>/",
        views.delete_class,
        name="delete_class"
    ),
    path(
        "manage/attendance/<int:class_id>/",
        views.manage_attendance,
        name="manage_attendance"
    ),
]
