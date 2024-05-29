from urllib import request

from django.http import HttpResponseRedirect

from recipes.models import Recipe
from recipes.views import YoursPageView
from .models import Cook
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView


# Create your views here.
class RecipeSignUpView(CreateView):
    form_class = UserCreationForm
    template_name = "registration/signup.html"


class RecipeLoginView(LoginView):
    success_url = reverse_lazy("/accounts/login")
    template_name = "registration/login.html"


class FavouritesPageView(YoursPageView):
    template_name = "../templates/favourites.html"

    def get_queryset(self):
        queryset = Cook.objects.get(title=self.request.user).favourites.all()
        return queryset


def favourite_add(request, pk):
    cook = Cook.objects.get(title=request.user)
    favourites=cook.favourites.all()
    if favourites.filter(pk=pk).exists():
        cook.favourites.remove(pk)
    else:
        cook.favourites.add(pk)
    return HttpResponseRedirect(reverse('home'))



