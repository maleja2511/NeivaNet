from django.urls import path
from . import views
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from .views import RegisterView, UserProfileView
from .views import update_profile

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("", LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("profile/<int:user_id>/", UserProfileView.as_view(), name="profile"),
    path("update_profile/", update_profile, name="update_profile"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "password_reset/",
        PasswordResetView.as_view(
            template_name="accounts/registration/password_reset_form.html",
            email_template_name="accounts/registration/password_reset_email.html",
            subject_template_name="accounts/registration/password_reset_subject.txt",
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        PasswordResetDoneView.as_view(
            template_name="accounts/registration/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="accounts/registration/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        PasswordResetCompleteView.as_view(
            template_name="accounts/registration/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
