from django.contrib.auth import login, authenticate, REDIRECT_FIELD_NAME
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.views.generic.base import ContextMixin
from .forms import SignUpForm
from django.contrib import messages
from django.urls import reverse_lazy


class SignUpView(FormView):
    template_name = 'accounts/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('accounts:registered')

    def form_valid(self, form):
        form.save()

        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')

        user = authenticate(username=username, password=raw_password)
        login(self.request, user)

        messages.add_message(self.request, messages.SUCCESS,
                             'You are successfully registered!')

        return super(SignUpView, self).form_valid(form)


class SignUpSuccess(TemplateView):
    template_name = 'accounts/signup_success.html'
