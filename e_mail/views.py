from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import EmailComposeForm
from django.core.mail import send_mail

# Create your views here.
class EmailInbox(LoginRequiredMixin,TemplateView):
    template_name = "email/email-inbox.html"
class EmailRead(LoginRequiredMixin,TemplateView):
    template_name = "email/email-read.html"
#class EmailCompose(LoginRequiredMixin,TemplateView):
    #template_name = "email/email-compose.html"


def EmailCompose(request):
    if request.method == 'POST':
        form = EmailComposeForm(request.POST)
        if form.is_valid():
            # Process the form data and send the email
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            recipients = form.cleaned_data['recipients']
            send_mail(subject, message, 'your_email@example.com', recipients)
            return redirect('email_sent')
    else:
        form = EmailComposeForm()
    return render(request, 'email/email-compose.html', {'form': form})
