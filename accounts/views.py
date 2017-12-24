from django.contrib.auth import login, authenticate, REDIRECT_FIELD_NAME
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.views.generic.base import ContextMixin
from .forms import SignUpForm, LoginForm
from django.contrib import messages
from django.urls import reverse_lazy
# from django.contrib.messages.views import SuccessMessageMixin


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
