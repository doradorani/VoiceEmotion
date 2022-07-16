from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")
    class Meta:
        model = User
        fields = (
            'username',
            'password1',
            'password2',
            'email',
            'genres',
            'gender',
            'year',
            'month',
            'day',
            )
