from django import forms
from django.contrib.auth.models import User

class EditUser(forms.ModelForm):
    first_name = forms.CharField(max_length=500, required=True)
    class Meta:
        model = User
        fields = ('first_name','username','email')