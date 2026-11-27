from django import forms
from django.contrib.auth.forms import (
    BaseUserCreationForm,
    UserChangeForm
)

from .models import User

class CustomUserCreationForm(BaseUserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("email","phone_number","first_name","last_name",)
        
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = "__all__"