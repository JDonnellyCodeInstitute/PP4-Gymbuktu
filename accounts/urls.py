from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    # User Authentication
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        template_name='accounts/logout.html'
    ), name='logout'),

    # Profile & Email Verification
    path('profile/', views.profile, name='profile'),
    path('check-email/', views.check_email, name='check_email'),
    path('verify/<uuid:token>/', views.verify_email, name='verify_email'),
    path('already-verified/', views.already_verified, name='already_verified'),

    # Password Reset
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset.html'
    ), name='password_reset'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'
    ), name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
          template_name='accounts/password_reset_confirm.html'
         ), name='password_reset_confirm'),

    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
            template_name='accounts/password_reset_complete.html'
         ), name='password_reset_complete'),
]
