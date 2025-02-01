from django.urls import path
from . import views

urlpatterns = [
    path('', views.feedback_view, name='feedback'),
    path('received/', views.feedback_received, name='feedback_received'),
]