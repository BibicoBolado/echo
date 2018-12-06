from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from .forms import Contact

# Create your views here.

def index(request):
    template_name='index.html'
    return render(request,template_name)
    
def contact(request):
        template_name='contact.html'
        context={}

        if request.method=='POST':
            form = Contact(request.POST)
            if form.is_valid():
                context['is_valid']=True
                print(form.cleaned_data['name'])
                
                form.mail(  form.cleaned_data['name'],
                            form.cleaned_data['email'],
                            form.cleaned_data['message'],
                            form.cleaned_data['phone'],
                        )
                messages.success(request,'O primeiro passo foi dado, verifique seu e-mail e vamos lá!')

                form= Contact()
        else:
            form=Contact()
        context['form'] = form

        return render(request,template_name,context)