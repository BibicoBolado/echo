from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class Profile(models.Model):
    user    = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    name    = models.CharField('Nome*', max_length=150,null=True)
    phone   = models.IntegerField('Número*',null=True)
    ingress = models.IntegerField('Número Acessos',null=True)

    def __str__(self):
        return "Nome : {} Número {}".format(self.name,self.phone)
    
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
    
    class Meta:
        verbose_name        = "Perfil"
        verbose_name_plural = "Perfis"

class PasswordReset(models.Model):
    user        =   models.ForeignKey(User,verbose_name='Usuário'
                    ,on_delete=models.CASCADE,blank=True,null=True,related_name='resets')
    #NO MOMENTO QUE EU FOR CHAMAR OS PASSWORDS DENTRO DE USER EU CHAMO User.resets.all()
    #SE  NÃO FOSSE    PELO  related_name  EU CHAMARIA  POR  User.passwordreset_Set.all()
    key         =   models.CharField('Chave',max_length=100,unique=True)
    created_at  =   models.DateTimeField('Criado em',auto_now_add=True)
    confirmed   =   models.BooleanField('Confirmado?',default=False,blank=True)

    def __str__(self):
        return '{} - {}'.format(self.user,self.created_at)
    class Meta:
        verbose_name        = 'Nova Senha'
        verbose_name_plural = 'Novas Senhas'
        ordering            = ['-created_at']