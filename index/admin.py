from django.contrib import admin
from .models import Projet,Image

class ProjetAdmin(admin.ModelAdmin):
    list_display        = ['name','created']
    search_fields       = ['name']
    list_filter         = ['created']
    prepopulated_fields = {"slug":("name",)}

class ImageAdmin(admin.ModelAdmin):
    list_display        = ['projet','name']
    search_fields       = ['name']
    list_filter         = ['projet']

admin.site.register(Projet,ProjetAdmin)
admin.site.register(Image,ImageAdmin)