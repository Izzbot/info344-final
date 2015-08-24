from django import forms
from .models import Comparison

class ComparisonForm(forms.ModelForm):
    class Meta:
        model = Comparison
        fields = ('profile_url',)