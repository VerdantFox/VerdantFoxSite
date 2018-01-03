from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView
from .forms import SignUpForm, LoginForm, EditUserForm, EditProfileForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.db import transaction
from .models import UserProfile
from django.shortcuts import render, redirect


class SignUpView(FormView):
    template_name = 'accounts/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.save()

        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')

        user = authenticate(username=username, password=raw_password)
        login(self.request, user)

        messages.add_message(
            self.request, messages.SUCCESS,
            'Welcome {}, you have successfully registered!'.format(username))

        return super(SignUpView, self).form_valid(form)


class LoginView(FormView):
    template_name = 'accounts/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password')

        user = authenticate(username=username, password=raw_password)
        login(self.request, user)

        messages.add_message(
            self.request, messages.SUCCESS,
            'Welcome {}, you are now logged in!'.format(username))

        return super(LoginView, self).form_valid(form)


@login_required
def view_profile(request):
    user = request.user
    profile = UserProfile.objects.get(user=user)
    return render(request, 'accounts/view_profile.html', {
        'user': user,
        'profile': profile,
    })


@login_required
@transaction.atomic
def edit_profile(request):
    if request.method == 'POST':
        user_form = EditUserForm(request.POST, instance=request.user)
        profile_form = EditProfileForm(request.POST, request.FILES,
                                       instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('accounts:view_profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = EditUserForm(instance=request.user)
        profile_form = EditProfileForm(instance=request.user.userprofile)
    return render(request, 'accounts/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
