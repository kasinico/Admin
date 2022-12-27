from django import forms




#email from
class EmailComposeForm(forms.Form):
    to = forms.EmailField(label='To')
    subject = forms.CharField(label='Subject')
    message = forms.CharField(label='Message', widget=forms.Textarea)