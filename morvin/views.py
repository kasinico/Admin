from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from allauth.account.views import PasswordSetView,PasswordChangeView
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from django.shortcuts import redirect, render, get_object_or_404

# relative import of forms
from .models import CrimeModel
from .forms import CrimeForm
from django.views.generic import DeleteView
from django.urls import reverse



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
    context ={}

    # VARIABLE TO HOLD RETURN VALUE, modelname.odel obj atrributes.all-method
    context["dataset"] = CrimeModel.objects.all()

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