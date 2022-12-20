from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from allauth.account.views import PasswordSetView,PasswordChangeView
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from django.shortcuts import redirect, render

# relative import of forms
from .models import CrimeModel
from .forms import CrimeForm


class Index(LoginRequiredMixin,TemplateView):
    template_name = "index.html"
    
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
    if request.method == "POST":  
        form = CrimeForm(request.POST)  
        if form.is_valid():  
            try:  
                form.save()  
                return redirect('/list_view')  
            except:  
                pass  
    else:  
        form = CrimeForm()  
    return render(request,'addcrime.html',{'form':form})  

#list/show crime view
def list_view(request):
	# dictionary for initial data with
	# field names as keys
	context ={}

	# VARIABLE TO HOLD RETURN VALUE, modelname.odel obj atrributes.all-method
	context["dataset"] = CrimeModel.objects.all()
	
    	
	return render(request, "list_view.html", context)


#edit member crime
def edit(request, id): 
    context = {} 
    context["dataset"] = CrimeModel.objects.get(id=id)  
    return render(request,'edit.html', context)  