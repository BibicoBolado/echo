from django.urls import path
from .import views

app_name='index'
urlpatterns = [

    path('',views.index,name='index'),
    path('contato/',views.contact,name='contact'),
    path('portfolio/',views.portfolio,name='portifolio'),
    path('portfolio/<slug:slug>',views.project,name='project'),

]