from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile,PasswordReset

from .utils import generate_hash_key
from index.mail import send_mail_user

class RegisterForm(UserCreationForm):
    username    =  forms.CharField(label='Usuário',max_length=150,
                widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Login'}))
    email       =  forms.EmailField(label='Email',max_length=250,
                widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Email'}))
    password1   =  forms.CharField(label='Senha',max_length=32,
                widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Senha'}))
    password2   =  forms.CharField(label='Confirmar Senha',max_length=32,
                widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Senha'}))
    
    def clean_email(self):
        email   = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email já Cadastrado')
        return email
    def save(self,commit=True):
        print("********************************AQUI**********************************")
        user        =super(RegisterForm,self).save(commit=False)
        user.email   =self.cleaned_data['email']
        if commit:
            user.save()
        return user

class ProfileForm(forms.ModelForm):
    class Meta:
        model   = Profile
        fields  = ('name','phone')

class Login(forms.Form):
    userNameLogin   =   forms.CharField(label='Login',max_length=150,
                        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Login'}))
    passwordLogin =     forms.CharField(label='Senha',max_length=32, 
                        widget=forms.PasswordInput(attrs={'class' : 'form-control','placeholder': 'Senha'}))

class PasswordResetForm(forms.Form):
    email   = forms.EmailField(label='E-mail',max_length=100,
            widget=forms.TextInput(attrs={'class':'form-control','placeholder':'email'})
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            return email
        raise forms.ValidationError("Nenhum Usuário Encontrado com Esse E-mail")
    #toda função clean_X retorna o valor que   o 
    #formulário estará pegando no final p salvar
    def save(self):
        email = self.cleaned_data['email']
        user = User.objects.get(email=email)
        key = generate_hash_key(email)
        reset = PasswordReset(key=key,user=user)
        reset.save()
        template_name='reset_password_mail.html'
        subject = 'Nova  Senha Studio <echo>'
        context = {'Usuario':user.username,'reset':reset}
        print(reset)
        send_mail_user(subject,template_name,context,[user.email])
        