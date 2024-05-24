from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CustomUserCreationForm
# Create your views here.



class SignUpView(CreateView):
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"