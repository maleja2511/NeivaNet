from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile
from django.core.exceptions import ValidationError

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def clean_email(self):
        # Obtén el correo electrónico proporcionado en el formulario
        email = self.cleaned_data['email']

        # Verifica si ya existe un usuario con ese correo electrónico
        if User.objects.filter(email=email).exists():
            raise ValidationError("Ya existe un usuario con ese correo electrónico.")

        return email


class UserProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'date_of_birth']