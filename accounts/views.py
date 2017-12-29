from django.contrib.auth import login, authenticate, REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.views.generic import TemplateView, DetailView, ListView
from django.views.generic.base import ContextMixin
from .forms import SignUpForm, LoginForm, EditUserForm, EditProfileForm
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.db import transaction
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
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


class SignUpSuccess(TemplateView):
    template_name = 'accounts/signup_success.html'


class LoginView(FormView):
    template_name = 'accounts/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        # form.save()

        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password')

        user = authenticate(username=username, password=raw_password)
        login(self.request, user)

        messages.add_message(
            self.request, messages.SUCCESS,
            'Welcome {}, you are now logged in!'.format(username))

        return super(LoginView, self).form_valid(form)


@login_required
def view_profile(request,):
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
        user_form = EditUserForm(request.POST)
        profile_form = EditProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,
                             _('Your profile was successfully updated!'))
            return redirect('settings:profile')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = EditUserForm()
        profile_form = EditProfileForm()
    return render(request, 'accounts/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })



# def view_profile(request, pk=None):
#     if pk:
#         user = User.objects.get(pk=pk)
#     else:
#         user = request.user
#     args = {'user': user}
#     return render(request, 'accounts/profile.html', args)
#
#
# def edit_profile(request):
#     if request.method == 'POST':
#         form = EditProfileForm(request.POST, instance=request.user)
#
#         if form.is_valid():
#             form.save()
#             return redirect(reverse('accounts:view_profile'))
#     else:
#         form = EditProfileForm(instance=request.user)
#         args = {'form': form}
#         return render(request, 'accounts/edit_profile.html', args)


