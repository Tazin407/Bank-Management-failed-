from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import FormView, UpdateView
from django.contrib.auth import login, logout
from .import forms
from .import models
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views import View
# Create your views here.

class UserRegistrationView(FormView):
    template_name='user_registration.html'
    form_class=forms.UserRegistrationForm
    success_url= reverse_lazy('register')
    
    def form_valid(self, form):
        user= form.save()
        login(self.request, user)
        return super().form_valid(form)
    #shob thik thakle ashol function call hobe

class UserLoginView(LoginView):
    template_name='user_login.html'
    def get_success_url(self) -> str:
        return reverse_lazy('profile')
    
class UserLogoutView(LogoutView):
    def get_success_url(self):
        if self.request.user.is_authenticated:
            logout(self.request)
        
        return reverse_lazy('home')
    
# class ProfileView(UpdateView):
#     model= models.User
#     form_class=forms.UserUpdateForm
#     template_name='profile.html'
    
#     def get_success_url(self) -> str:
#         return reverse_lazy('profile')
    
class ProfileView(View):
    template_name= 'profile.html'
    
    def get(self, request):
        form= forms.UserUpdateForm(instance= self.request.user)
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form= forms.UserUpdateForm(request.POST, instance= request.user)
        
        if form.is_valid():
            form.save()
            # return redirect('profile')
        
        return render(request, self.template_name, {'form': form})

