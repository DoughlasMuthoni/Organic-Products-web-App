
from django import forms
from django.contrib.auth.forms import UserCreationForm
from user_authens.models import Profile, User



class UserRegisterForm(UserCreationForm):
    # Add Bootstrap class to form fields
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            "placeholder": "Username",
            "class": "form-control"
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "placeholder": "Email",
            "class": "form-control"
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": "Password",
            "class": "form-control"
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": "Confirm password",
            "class": "form-control"
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileForm(forms.ModelForm):
    full_name = forms.CharField(
        widget=forms.TextInput(attrs={
            "placeholder": "FullName",
            "class": "form-control"
        })
    )


    bio = forms.CharField(
        widget=forms.TextInput(attrs={
            "placeholder": "Bio",
            "class": "form-control"
        })
    )
    phone = forms.CharField(
        widget=forms.TextInput(attrs={
            "placeholder": "Phone",
            "class": "form-control"
        })
    )
    class Meta:
        model = Profile
        fields = [ 'image', 'full_name', 'bio', 'phone']