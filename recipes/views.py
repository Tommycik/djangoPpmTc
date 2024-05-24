from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Recipe
from django.views.generic import ListView, DetailView, FormView  # new
# Create your views here.
class RecentPageView(ListView):
    model = Recipe
    template_name = "../templates/recent.html"

class DetailPageView(DetailView):
    model = Recipe
    template_name = "../templates/detail.html"
class SearchPageView(ListView):
    model = Recipe
    template_name = "../templates/recent.html"

