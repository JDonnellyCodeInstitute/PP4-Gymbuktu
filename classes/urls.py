from django.urls import path
from . import views

urlpatterns = [
    path("", views.class_list, name="class_list"),
    path("<int:class_id>/", views.class_detail, name="class_detail"),
    path("<int:class_id>/book/", views.book_class, name="book_class"),
    path("cancel/<int:booking_id>/", views.cancel_booking, name="cancel_booking"),
]