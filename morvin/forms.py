from django.forms import ModelForm
from django import forms
from .models import CrimeModel


class CrimeForm(ModelForm):
    class Meta:
        model = CrimeModel
        fields = '__all__'

       