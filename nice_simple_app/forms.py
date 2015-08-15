from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        models = Profile
        fields = ('img_url')