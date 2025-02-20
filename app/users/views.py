import threading

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.models import Site
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views.generic import DetailView, UpdateView
from users.models import User

from .forms import UserCustomCreationForm, UserUpdateForm
from .models import User
from .tasks import user_registration_email
from .tokens import account_activation_token


class UserLoginView(auth_views.LoginView):
    template_name = "users/login.html"

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            messages.info(self.request, f"Your are already logged in {request.user}")
            return redirect(reverse_lazy("list"))  # Redirect to the home page
        return super().get(request, *args, **kwargs)


class UserChangePasswordView(auth_views.PasswordChangeView):
    template_name = "users/change_password.html"


class UserPasswordChangeDoneView(auth_views.PasswordChangeDoneView):
    template_name = "users/change_password_done.html"


class UserPasswordResetView(auth_views.PasswordResetView):
    template_name = "users/password_reset.html"

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            messages.info(self.request, f"Your are already logged in {request.user}")
            return redirect(reverse_lazy("list"))  # Redirect to the home page
        return super().get(request, *args, **kwargs)


class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = "users/password_reset_done.html"

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            messages.info(self.request, f"Your are already logged in {request.user}")
            return redirect(reverse_lazy("list"))  # Redirect to the home page
        return super().get(request, *args, **kwargs)


class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = "users/password_reset_confirm.html"

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            messages.info(self.request, f"Your are already logged in {request.user}")
            return redirect(reverse_lazy("list"))  # Redirect to the home page
        return super().get(request, *args, **kwargs)


class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = "users/password_reset_complete.html"

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            messages.info(self.request, f"Your are already logged in {request.user}")
            return redirect(reverse_lazy("list"))  # Redirect to the home page
        return super().get(request, *args, **kwargs)


def logout_view(request):
    logout(request)
    return redirect("login")


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect("/")
    else:
        return redirect("login")


@login_required
def user_registration_view(request):
    current_site = Site.objects.get_current()
    domain = current_site.domain
    if request.method == "POST":
        form = UserCustomCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            to_email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password1")
            user.is_active = False
            user.save()
            user_registration_email_thread = threading.Thread(
                target=user_registration_email,
                args=(request, user, to_email, password),
            )
            user_registration_email_thread.start()
    else:
        form = UserCustomCreationForm()
    return render(request, "users/register.html", {"form": form})


#


@login_required
def user_update(request):
    user = get_object_or_404(User, pk=request.user.pk)

    if request.method == "POST":
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect(
                "user-detail",
            )  # Redirect to a user detail or other page
    else:
        form = UserUpdateForm(instance=user)

    return render(request, "users/user_form.html", {"form": form, "user": user})


@login_required
def user_detail(request):
    if request.user.role == "admin" or request.user.role == "agent":
        user = get_object_or_404(User, pk=request.user.id)
    else:
        user = get_object_or_404(User, pk=request.user.id)
    return render(request, "users/user_detail.html", {"user": user})
