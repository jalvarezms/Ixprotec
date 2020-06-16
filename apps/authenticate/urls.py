# movies/urls.py
from django.urls import path
from .views import *

app_name = "authenticate" #Namespace v3 Django

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

]