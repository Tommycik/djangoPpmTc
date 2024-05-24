from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView


# Create your views here.
class SignUpView(CreateView):
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

class RecipeLoginView(LoginView):
    template_name = "registration/login.html"