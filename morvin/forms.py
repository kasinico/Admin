from django.forms import ModelForm
from django import forms
from .models import CrimeModel


class CrimeForm(forms.ModelForm):
    class Meta:
        model = CrimeModel
        fields = ['name', 'crime_type', 'license', 'occupation', 'stage', 'telephone', 'custody']

    custody = forms.ChoiceField(choices=CrimeModel.CUSTODY_CHOICES)