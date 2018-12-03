from django.template.loader import render_to_string
#Ele faz a rendereziação de um template e gera uma string
from django.template.defaultfilters import striptags
#Striptags remove as TAGS do html <>
from django.core.mail import EmailMultiAlternatives
#Uma class que representa um email com var

from django.conf import settings

def send_mail_user(subject,template_name,context,recipient_list,
    from_email=settings.EMAIL_HOST_USER,fail_silently=False):

    message_html = render_to_string(template_name,context)
    message_txt=striptags(message_html)
    email = EmailMultiAlternatives(
        subject=subject,body=message_txt,from_email=from_email,
        to=recipient_list
    )
    email.attach_alternative(message_html,"text/html")
    #Essa parte que é o alternative, os leitores de email já renderizam isso direto
    email.send(fail_silently=fail_silently)