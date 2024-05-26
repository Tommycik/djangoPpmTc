from urllib import request

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView


# Create your views here.
class RecipeSignUpView(CreateView):
    form_class = UserCreationForm
    #reverse_lazy("accounts:login")
    template_name = "registration/signup.html"


class RecipeLoginView(LoginView):
    success_url = reverse_lazy("/accounts/login")
    template_name = "registration/login.html"



