from django.urls import path
from .import views

app_name='accounts'
urlpatterns = [

    path('',views.gate,name='gate'),
    path('login/',views.log,name='login'),
    path('registrar/',views.regView,name='regView'),
    path('logout',views.leave,name='leave'),
    path('registrar-usuario/',views.regUser,name='regUser'),
    path('recuperar-senha/',views.password_reset,name='password_reset'),

]