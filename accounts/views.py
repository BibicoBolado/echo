from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate, get_user_model
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import PasswordReset
from .utils import generate_hash_key
# Create your views here.

User = get_user_model()

def gate(request):
    template_name   ='gate.html'
    form            = Login()
    context         = {'form':form}
    return render (request,template_name,context)

def log(request):
    context={}
    if request.method=='POST':
        form = Login(request.POST)
        if form.is_valid():
            context['is_valid']   =True
            username            =form.cleaned_data['userNameLogin']
            password            =form.cleaned_data['passwordLogin']
            user                =authenticate(request,username=username,password=password)

            if user is not None:
                login(request,user)
                return redirect('index:index')
            else:
                print(user)
                messages.warning(request,'Usuário ou Senha Inválidos')
                return redirect('accounts:gate')
    else:
        pass

def regView(request):
    template_name       ="register.html"
    context={}
    form1               =RegisterForm()
    form2               =ProfileForm()
    context['formReg']  = form1
    context['formProf'] = form2

    return render(request,template_name,context)

def regUser(request):
    if request.method == 'POST':
        form  = RegisterForm(request.POST)

        form2 = ProfileForm(request.POST)
        if form.is_valid():  
            user = form.save()
            user=authenticate(
                username=user.username,
                password=form.cleaned_data['password1']
                )
            login(request,user)
            if form2.is_valid():
                request.user.profile.name = form2.cleaned_data['name']
                request.user.profile.phone= form2.cleaned_data['phone']
                request.user.profile.save()
                return redirect('index:index')
        else:
            print(form.errors )
            messages.warning(request, form.errors)
            return redirect('accounts:regView')
    else:
        pass

def password_reset(request):
    template_name   ='passwordReset.html'
    context         ={}
    form            =PasswordResetForm(request.POST or None)
    #or None   ve se request.POST é vazio e trata o 
    # a   chamada como  form =  PasswordResetForm()
    # e com o form vazio ps form.is_valid() é falso
    if request.method=='POST':
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            key = generate_hash_key(email)
            reset = PasswordReset(key=key,user=user)
            reset.save()
            messages.success(request,'Verifique seu Email')
        else:
            messages.warning(request,form.errors)
    context['form'] =form
    return render(request,template_name,context)


@login_required
def leave(request):
    logout(request)
    return redirect('index:index')