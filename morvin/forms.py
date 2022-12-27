from django.forms import ModelForm
from django import forms
from .models import CrimeModel


class CrimeForm(forms.ModelForm):
    class Meta:
        model = CrimeModel
        fields = ['name', 'crime_type', 'license', 'occupation', 'stage', 'telephone', 'custody']

    custody = forms.ChoiceField(choices=CrimeModel.CUSTODY_CHOICES)



#chat form
class ChatMessageForm(forms.Form):
    sender = forms.CharField(max_length=200)
    message = forms.CharField(widget=forms.Textarea)




#email from
class EmailComposeForm(forms.Form):
    to = forms.EmailField(label='To')
    subject = forms.CharField(label='Subject')
    message = forms.CharField(label='Message', widget=forms.Textarea)