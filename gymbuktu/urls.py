"""
URL configuration for gymbuktu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from classes.views import classes_test
from facilities.views import facilities_test
from feedback.views import feedback_test
from base_static.views import static_test
from gym_goers.views import gym_goers_test

urlpatterns = [
    path('classes/', classes_test, name='classes'),
    path('facilities/', facilities_test, name='facilities'),
    path('feedback/', feedback_test, name='feedback'),
    path('base_static/', static_test, name='base_static'),
    path('gym_goers/', gym_goers_test, name='gym_goers'),
    path('admin/', admin.site.urls),
]
