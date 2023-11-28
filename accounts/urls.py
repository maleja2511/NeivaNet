from django.urls import path
from django.contrib.auth.views import (
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from .views import RegisterView, UserProfileView, CustomPasswordResetView, update_profile, CustomLoginView
from accounts import views

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("", CustomLoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("profile/<int:user_id>/", UserProfileView.as_view(), name="profile"),
    path("update_profile/", update_profile, name="update_profile"),
    path("logout/", LogoutView.as_view(next_page='/'), name="logout"),
    path(
    "password_reset/<str:from_where>/",
    CustomPasswordResetView.as_view(),
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
    path('confirm_email/<uuid:token>/', views.confirm_email, name='confirm_email'),
]
