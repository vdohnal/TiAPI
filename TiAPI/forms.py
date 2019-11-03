from django import forms
from django.contrib.auth.models import User


class TokenLoginForm(forms.Form):
    token = forms.CharField(label='Login token')


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=User._meta.get_field('username').max_length)
    password = forms.CharField(min_length=6, widget=forms.PasswordInput())
    next = forms.URLField(required=False, widget=forms.HiddenInput())
