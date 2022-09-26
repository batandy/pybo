from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm

class UserCreateForm(UserCreationForm):
    email=forms.EmailField(label="이메일")

    class Meta:
        model=User
        fields=("username", "email")

