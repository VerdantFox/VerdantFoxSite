from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from .forms import SignUpForm, LoginForm, EditUserForm, EditProfileForm, GetUsernameForm
from django.urls import reverse_lazy
from django.db import transaction
from .models import UserProfile
from django.shortcuts import render, redirect
from social_django.models import UserSocialAuth
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.signals import user_logged_out, user_logged_in
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect


# https://stackoverflow.com/questions/46542502/django-how-to-add-a-logout-successful-message-using-the-django-contrib-auth
def show_logout_message(sender, user, request, **kwargs):
    messages.info(request, "You have logged out.")


def show_login_message(sender, user, request, **kwargs):
    user = request.user
    messages.success(request, f"Welcome {user}, you are now logged in.")


user_logged_out.connect(show_logout_message)
user_logged_in.connect(show_login_message)


class SignUpView(FormView):
    template_name = "accounts/signup.html"
    form_class = SignUpForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.save()

        username = form.cleaned_data.get("username")
        raw_password = form.cleaned_data.get("password1")

        user = authenticate(username=username, password=raw_password)
        login(self.request, user)

        return super(SignUpView, self).form_valid(form)


class LoginView(FormView):
    template_name = "accounts/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        raw_password = form.cleaned_data.get("password")

        user = authenticate(username=username, password=raw_password)
        login(self.request, user)

        return super(LoginView, self).form_valid(form)


@login_required
def view_profile(request):
    user = request.user
    profile = UserProfile.objects.get(user=user)
    return render(
        request, "accounts/view_profile.html", {"user": user, "profile": profile,}
    )


@login_required
@transaction.atomic
def edit_profile(request):
    if request.method == "POST":
        user_form = EditUserForm(request.POST, instance=request.user)
        profile_form = EditProfileForm(
            request.POST, request.FILES, instance=request.user.userprofile
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile was successfully updated!")
            return redirect("accounts:view_profile")
        else:
            messages.error(request, "Please correct the error below.")
    else:
        user_form = EditUserForm(instance=request.user)
        profile_form = EditProfileForm(instance=request.user.userprofile)
    return render(
        request,
        "accounts/edit_profile.html",
        {"user_form": user_form, "profile_form": profile_form},
    )


@login_required
def settings(request):

    user = request.user

    if request.method == "POST":
        if "delete-account" in request.POST:
            user.delete()
            messages.info(request, "Your account has been deleted!")
            return redirect("home")

    try:
        github_login = user.social_auth.get(provider="github")
    except UserSocialAuth.DoesNotExist:
        github_login = None

    try:
        twitter_login = user.social_auth.get(provider="twitter")
    except UserSocialAuth.DoesNotExist:
        twitter_login = None

    try:
        facebook_login = user.social_auth.get(provider="facebook")
    except UserSocialAuth.DoesNotExist:
        facebook_login = None

    can_disconnect = user.social_auth.count() > 1 or user.has_usable_password()

    return render(
        request,
        "accounts/settings.html",
        {
            "github_login": github_login,
            "twitter_login": twitter_login,
            "facebook_login": facebook_login,
            "can_disconnect": can_disconnect,
        },
    )


@login_required
def password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == "POST":
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Your password was successfully updated!")
            return redirect("accounts:password")
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = PasswordForm(request.user)
    return render(request, "accounts/password.html", {"form": form})


class CustomPasswordResetView(PasswordResetView):
    email_template_name = "accounts/reset/password_reset_email.html"
    subject_template_name = "accounts/reset/password_reset_subject.txt"
    success_url = reverse_lazy("accounts:password_reset_done")
    template_name = "accounts/reset/password_reset_form.html"


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy("accounts:password_reset_complete")
    template_name = "accounts/reset/password_reset_confirm.html"
