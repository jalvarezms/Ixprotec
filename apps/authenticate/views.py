from django.shortcuts import render, HttpResponseRedirect, reverse, redirect
from django.http import HttpResponse
from django.views.generic import FormView, TemplateView, RedirectView, View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.employees.models import Employee

# Create your views here.

class LoginView(FormView):    
    form_class = AuthenticationForm
    template_name = "login.html"
    #success_url = ''
    """ def dispatch(self, request, *args, **kwargs):
        if  not request.user.is_anonymous:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(LoginView, self).dispatch(request, *args, **kwargs)
    """
    def form_valid(self, form):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:        
            login(self.request, form.get_user())            
        return super(LoginView, self).form_valid(form)        

    def get_success_url(self):
        return reverse_lazy('base:index')    

class LogoutView(LoginRequiredMixin, RedirectView):
    is_permanent = True

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)
    
    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy('authenticate:login')        