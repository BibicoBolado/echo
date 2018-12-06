from django.db import models

# Create your models here.

class Projet(models.Model):
    name =          models.CharField('Nome',max_length=150)
    slug =          models.SlugField('Atalho',max_length=150)
    description =   models.TextField('Descrição')
    created =       models.DateTimeField('Criado em',auto_now_add=True)
    modified =      models.DateTimeField('Atualiado em',auto_now=True)

    imageMin =      models.ImageField(upload_to = 'catalog/imagensmin',
                    verbose_name='Imagem',blank=True,null=True)
    
    link    =       models.CharField('Link Site',max_length=150,default=" ")
    tipo    =       models.CharField('Tipo Projeto',max_length=50,default=" ")

    class Meta:
        verbose_name='Projeto'
        verbose_name_plural = 'Projetos'
        ordering = ['name']
    def __str__(self):
        return self.name

class Image(models.Model):
    projet =        models.ForeignKey('index.Projet',verbose_name='Fotos',on_delete=models.CASCADE,
                    related_name='fotos')
    name   =        models.CharField('Nome',max_length=150)
    description =   models.TextField('Descrição')
    image       =   models.ImageField(upload_to = 'catalog/imagens',
                    verbose_name='Imagem',blank=True,null=True)
    
    class Meta:
        verbose_name = 'Imagem'
        verbose_name_plural = 'Imagens'
    def __str__(self):
        return self.name