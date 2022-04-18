from django import forms
from django.contrib.auth import get_user_model
<<<<<<< HEAD
=======
from django.contrib.auth.forms import UserCreationForm

>>>>>>> 1e087b7b9f9c4e9cb0766098ad60ead1921cdd7a
User = get_user_model()

class UserForm(UserCreationForm):
    email = forms.EmailField(label='이메일')

    class Meta:
        model = User
        fields = ("username","email")