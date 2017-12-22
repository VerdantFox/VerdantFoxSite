from datetime import timedelta

from django import forms
from django.contrib.auth import REDIRECT_FIELD_NAME, get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from django.db.models import Q
from django.utils.translation import gettext_lazy as _


UserModel = get_user_model()


class SignUpForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('username', 'first_name', 'last_name', 'email',
                  'password1', 'password2',)

    username = forms.CharField(
        label=_('Username'), max_length=50, required=True,
        help_text=_('Required. 150 characters or fewer. Letters, '
                    'digits and @/./+/-/_ only.'),
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(
        label=_('First Name'), max_length=50, required=False,
        help_text=_('Optional.'), widget=forms.TextInput(
            attrs={'class': 'form-control'}))
    last_name = forms.CharField(
        label=_('Last Name'), max_length=50, required=False,
        help_text=_('Optional.'),
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(
        label=_('Email'), max_length=255, required=True,
        help_text=_('Required. Type a valid email address.'),
        widget=forms.EmailInput(
            attrs={'placeholder': 'example@gmail.com',
                   'class': 'form-control'}))
    password1 = forms.CharField(
        label=_('Password:'), max_length=50, required=True,
        help_text=_("<ul><li>Your password can't be too similar "
                    "to your other personal information </li>"
                    "<li>Your password must contain at least 8 characters.</li>"
                    "<li>Your password can't be a commonly used password.</li>"
                    "<li>Your password can't be entirely numeric.</li></ul>"),
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(
        label=_('Password confirmation:'), max_length=50, required=True,
        help_text=_("Enter the same password as before, for verification."),
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    error_messages = {
        'unique_email': _('Email already in use.'),
    }

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()

        email = cleaned_data.get('email', '').lower()

        num_users = UserModel.objects.filter(email=email).count()
        if num_users > 0:
            self.add_error('email', self.error_messages['unique_email'])
