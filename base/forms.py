from django import forms
from django.contrib.auth.models import User
from .models import Profile,Snap,Comment

class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'bio']

class SnapForm(forms.ModelForm):
    class Meta:
        model = Snap
        fields = ['image', 'description','category']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class CaptionForm(forms.ModelForm):
    class Meta:
        model = Snap
        fields = ['description']