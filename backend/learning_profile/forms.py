from django.contrib.auth import get_user_model
from django import forms
from django.core.exceptions import ValidationError

User = get_user_model()


class CustomUserCreationForm(forms.Form):
    unikey = forms.CharField(label='Unikey', max_length=8)
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    def clean_unikey(self):
        unikey = self.cleaned_data['unikey'].lower()
        user = User.objects.filter(unikey=unikey)
        if user.count():
            raise ValidationError("This unikey has been already registered")
        return unikey

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        user = User.objects.filter(email=email)
        if user.count():
            raise ValidationError("This email has been already registered")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")
        return password2

    def save(self):
        user = User.objects.create_user(
            self.cleaned_data['unikey'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        return user
