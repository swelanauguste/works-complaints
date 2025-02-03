from django.urls import include, path

from . import views

urlpatterns = [
    # path("", include("django.contrib.auth.urls")),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path(
        "change-password/",
        views.UserChangePasswordView.as_view(),
        name="change-password",
    ),
    path(
        "change-password-done/",
        views.UserPasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    path("password-reset/", views.UserPasswordResetView.as_view(), name="password-reset"),
    path(
        "password-reset-done/",
        views.UserPasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
 
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        views.UserPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        views.UserPasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path("user-detail/", views.user_detail, name="user-detail"),
    path("user-update/", views.user_update, name="user-update"),
    path("register/", views.user_registration_view, name="register"),
    path("activate/<uidb64>/<token>/", views.activate, name="activate"),
]
