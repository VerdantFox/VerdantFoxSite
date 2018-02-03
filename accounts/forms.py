from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _
from .models import UserProfile
import pytz


UserModel = get_user_model()


class SignUpForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('username', 'email', 'password1', 'password2',)

    username = forms.CharField(
        label=_('Username'), max_length=50, required=True,
        help_text=_('Required. 150 characters or fewer. Letters, '
                    'digits and @/./+/-/_ only.'),
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Username'}))
    email = forms.EmailField(
        label=_('Email'), max_length=255, required=True,
        help_text=_('Required. Type a valid email address. Used for password '
                    'recovery.'),
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
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'placeholder': 'Password'}))
    password2 = forms.CharField(
        label=_('Password confirmation:'), max_length=50, required=True,
        help_text=_("Enter the same password as before, for verification."),
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'placeholder': 'Confirm password'}))

    error_messages = {
        'unique_email': _('Email already in use.'),
        'password_mismatch': _('Passwords do not match.')
    }

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()

        email = cleaned_data.get('email', '').lower()

        num_users = UserModel.objects.filter(email=email).count()
        if num_users > 0:
            self.add_error('email', self.error_messages['unique_email'])


class LoginForm(AuthenticationForm):
    class Meta:
        model = UserModel
        fields = ('username', 'password',)

    username = forms.CharField(
        label=_('Username:'), max_length=50, required=True,
        widget=forms.TextInput(attrs={'autofocus': 'autofocus',
                                      'class': 'form-control',
                                      'placeholder': 'Username'}))

    password = forms.CharField(
        label=_('Password:'), max_length=50, required=True,
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'placeholder': 'Password'}))
    error_messages = {
        'invalid_login': 'Username/password combination not found. '
                         'Note that both fields may be case-sensitive.'
    }


class EditUserForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ('username', 'email', 'first_name', 'last_name')
        # exclude = ('username',)

    username = forms.CharField(
        label=_('Username'), max_length=50, required=True,
        help_text=_('Required. 150 characters or fewer. Letters, '
                    'digits and @/./+/-/_ only.'),
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Username'}))

    email = forms.EmailField(
        label=_('Email:'), max_length=100, required=False,
        widget=forms.EmailInput(attrs={
            'placeholder': 'example@gmail.com',
            'autofocus': 'autofocus',
            'class': 'form-control'})
    )
    first_name = forms.CharField(
        label=_('First Name'), max_length=50, required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First Name'}))
    last_name = forms.CharField(
        label=_('Last Name'), max_length=50, required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last Name'}))


timezone_list = []

for timezone in pytz.common_timezones:
    timezone_list.append([timezone, timezone])


class EditProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('profile_picture', 'bio', 'location',
                  'timezone', 'birth_date')

    profile_picture = forms.ImageField(
        label=_('Profile Picture:'), required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control'}))
    bio = forms.CharField(
        label=_('About me:'), max_length=1000,
        required=False, widget=forms.Textarea(attrs={
            'placeholder': "What's your story? What exciting facts would you ",
            'class': 'form-control'}))
    location = forms.CharField(
        label=_('Location:'), max_length=100, required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'San Fransisco, CA'}))
    timezone = forms.TypedChoiceField(
        choices=timezone_list,
        empty_value=None, required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'}))
    birth_date = forms.DateField(
        label=_('Birth Date:'), required=False,
        widget=forms.DateInput(attrs={
            'placeholder': 'mm/dd/yyyy',
            'class': 'form-control'}))


class GetUsernameForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ('email',)

    email = forms.EmailField(
        label=_('Email'), max_length=255, required=True,
        help_text=_('Enter email associated with username'),
        widget=forms.EmailInput(
            attrs={'placeholder': 'example@gmail.com',
                   'class': 'form-control'}))
