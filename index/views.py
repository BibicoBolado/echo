from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.views.generic import ListView

from .forms import Contact
from .models import Projet

# Create your views here.

def index(request):
    template_name='index.html'
    return render(request,template_name)

###################ListView###################
    
#context_object_name= 'products'
#se eu não usar o código a cima
# o padrão será    product_list
#self.request - requisição
#self.kwargs - argumentos nomeados
#self.args - argumentos não nomeados da url
class portfolioList(ListView):
    template_name   = 'portifolio.html'
    paginate_by     = 100
    context_object_name= 'project'
    def get_queryset(self):
        project = Projet.objects.all()
        return project
    #def get_context_data(self,**kwargs):
    #    context  =   super(portfolioList
    #    ,self).get_context_data(**kwargs)
    #    context['category']=CategoryCatalog.objects.all()
    #    return context
    #    com a função acima eu posso colocar 
    #    quantos contextos quiser dentro da minha listview
portfolio=portfolioList.as_view()  

###################ListView###################

def project(request,slug):
    project = Projet.objects.get(slug=slug)
    print(project)
    context = {'project':project}
    template_name = 'project.html'
    return render(request,template_name,context)

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