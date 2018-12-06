from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login,logout,authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm,SetPasswordForm
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
            form.save()
            messages.success(request,'Verifique seu Email')
        else:
            messages.warning(request,form.errors)
    context['form'] =form
    return render(request,template_name,context)

def password_reset_confirm(request,key):
    template_name='password_change_form.html'
    context = {}
    reset = get_object_or_404(PasswordReset,key=key)
    form = SetPasswordForm(user=reset.user,data= request.POST or None)
    print(form)
    if request.method=='POST':
        if form.is_valid():
            form.save()
            messages.success(request,'Senha alterada com sucesso')
            return redirect('accounts:gate')
        else:
            messages.warning(request,form.errors)
    context['form']=form
    return render(request,template_name,context)


@login_required
def leave(request):
    logout(request)
    return redirect('index:index')