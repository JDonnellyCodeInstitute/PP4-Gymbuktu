from django.urls import path
from . import views

urlpatterns = [
    path('gym-rules/', views.gym_rules, name='gym_rules'),
]
