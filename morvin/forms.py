from django.forms import ModelForm
from django import forms
from .models import CrimeModel


class CrimeForm(forms.ModelForm):
    class Meta:
        model = CrimeModel
        fields = ['name', 'crime_type', 'license', 'occupation', 'stage', 'telephone', 'custody']

    custody = forms.ChoiceField(choices=CrimeModel.CUSTODY_CHOICES, required=True)

    def __init__(self, *args, **kwargs):
        super(CrimeForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['required'] = 'required'

    def as_form(self):
        return self._html_output(
            normal_row='<div class="form-group">{label}<div class="input-group">{field}{help_text}</div></div>',
            error_row='%s',
            row_ender='</div>',
            help_text_html='<span class="help-text">%s</span>',
            errors_on_separate_row=True)




#chat form
class ChatMessageForm(forms.Form):
    sender = forms.CharField(max_length=200)
    message = forms.CharField(widget=forms.Textarea)




#email from
class EmailComposeForm(forms.Form):
    to = forms.EmailField(label='To')
    subject = forms.CharField(label='Subject')
    message = forms.CharField(label='Message', widget=forms.Textarea)