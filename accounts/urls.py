from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from .forms import CustomLoginForm

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(
        template_name='accounts/login.html',
        authentication_form=CustomLoginForm
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('check-email/', views.check_email, name='check_email'),
    path('verify/<uuid:token>/', views.verify_email, name='verify_email'),
    path('already-verified/', views.already_verified, name='already_verified'),
]