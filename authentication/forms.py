from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class CreateUserForm(forms.Form, UserCreationForm):
    first_name = forms.CharField(max_length=500, required=True)
    class Meta:
        model = User
        fields = ('first_name','username', 'email', 'password1', 'password2')