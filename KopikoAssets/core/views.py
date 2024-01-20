from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth import login, logout

# Create your views here.
class Home(TemplateView):
    template_name='index.html'


    
    
