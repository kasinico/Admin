from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from allauth.account.views import PasswordSetView,PasswordChangeView
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from django.shortcuts import redirect, render, get_object_or_404

# relative import of forms
from .models import CrimeCount, CrimeModel

from .forms import CrimeForm
from .forms import EmailComposeForm
from .forms import ChatMessageForm
from django.views.generic import DeleteView
from django.urls import reverse
from .models import ChatMessage #chatmessages
from django.core.mail import send_mail
from django.core.paginator import Paginator





#class Index(LoginRequiredMixin,TemplateView):
    #template_name = "index.html"


#index page Dashboard with counter
def index(request):
    context = {}

    # Count the number of CrimeModel objects
    context['count'] = CrimeModel.objects.count()

    return render(request, 'index.html', context)

    
class Calendar(LoginRequiredMixin,TemplateView):
    template_name = "calendar.html"
#addcrime class
#class Addcrime(TemplateView):
    #template_name = "addcrime.html"
class Chat(LoginRequiredMixin,TemplateView):
    template_name = "chat.html"
class MyPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    success_url = reverse_lazy('index')
class MyPasswordSetView(LoginRequiredMixin, PasswordSetView):
    success_url = reverse_lazy('index')


#logic for add crime input
# ============================ Start functions for crud Addcrime ====================
"""def addcrime(request):
    # dictionary for initial data with
    # field names as keys
    context ={}
 
    # add the dictionary during initialization
    form = CrimeForm(request.POST or None)
    if form.is_valid():
        #instance = form.save(commit=False)
        #instance.user = request.user
        #instance.save()
        form.save()
    return HttpResponse(status=200)
    """
def addcrime(request):
    # create a new instance of CrimeModel
    my_model_instance = CrimeModel()
    if request.method == "POST":
        form = CrimeForm(request.POST, instance=my_model_instance)  
        if form.is_valid():  
            form.save()  
            return redirect('/list_view')  
    else:  
        form = CrimeForm(instance=my_model_instance)  
    return render(request,'addcrime.html',{'form':form})  
 

#list/show crime view
def list_view(request):
     # retrieve the object with the given pk
    # dictionary for initial data with
    # field names as keys
    paginator = Paginator(CrimeModel.objects.all(), 5) # 5 is the number of objects per page
    page = request.GET.get('page')
    objects = paginator.get_page(page)
    context ={}
    context["dataset"] = objects
    return render(request, "list_view.html", context)



#edit member crime
def edit(request, id):
    my_model_instance = get_object_or_404(CrimeModel, id=id)
    if request.method == 'POST':
        form = CrimeForm(request.POST, instance=my_model_instance)
        if form.is_valid():
            form.save()
            return redirect('list_view')
    else:
        form = CrimeForm(instance=my_model_instance)
    return render(request, 'edit.html', {'form': form})



#delete crime row
def delete(request, id):
    crime = get_object_or_404(CrimeModel, pk=id)
    crime.delete()
    return redirect('list_view')

# ============================ End functions for crud Addcrime ====================



#chat message
# ============================ Start functions for chat message ====================

def chat(request):
    messages = ChatMessage.objects.all()
    return render(request, 'chat.html', {'messages': messages})

def chat_view(request):
    # Get all chat messages in the database
    chat_messages = ChatMessage.objects.all()

    # Create an instance of the ChatMessageForm
    form = ChatMessageForm()

    # If the request method is POST, it means the form has been submitted
    if request.method == 'POST':
        # Bind the form data to the form instance
        form = ChatMessageForm(request.POST)
        # Check if the form is valid
        if form.is_valid():
            # Save the form data to the database
            form.save()
            # Redirect to the same page to show the updated list of chat messages
            return redirect('chat_view')

    # Render the chat view template, passing the form and chat_messages as context
    return render(request, 'chat.html', {'form': form, 'chat_messages': chat_messages})


