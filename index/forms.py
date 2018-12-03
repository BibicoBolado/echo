from django import forms
from django.core.mail import send_mail
from django.conf import settings
from datetime import date

from .mail import send_mail_user


class Contact(forms.Form):
    name    =  forms.CharField(label='Nome',max_length=100,
               widget=forms.TextInput(attrs={'class' : 'form-control','placeholder': 'Digite o Nome Aqui'})
    )
    email   =  forms.EmailField(label='Seu melhor e-mail',
               widget=forms.TextInput(attrs={'class' : 'form-control','placeholder': 'Digite o Email Aqui'})
    )
    phone   =  forms.CharField(label='Quer Receber uma Ligação?',max_length=150,
               widget=forms.TextInput(attrs={'class' : 'form-control','placeholder': '(xx)-91234-5678'})
    )
    message =  forms.CharField(label='Explique aqui sua ideia:',
               widget=forms.Textarea(attrs={'class' : 'form-control','placeholder': 'Deixe o Recado Aqui'})
    )
    def mail(self,name,email,message,phone):
        #Assunto Email Loja
        subject = 'Contato Echo {} | {}'.format(name,date.today())

        #Assunto Email User
        subjectUser = 'Olá %s, estamos quase lá!'%name

        menssagem = 'Nome: %s; Email: %s; Telefone: %s; Mensagem: %s' %(name,email,phone,message)
        send_mail(subject,menssagem,settings.EMAIL_HOST_USER ,[settings.CONTACT_EMAIL])

        context={
            'name':name,
            'email':email,
            'message':message,
        }
        template_name='mail/email.html'
        send_mail_user(subjectUser,template_name,context,[email])
        