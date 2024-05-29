from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import ListView, DetailView, FormView  # new


# Create your views here.
class HomePageView(TemplateView):
    template_name = "../templates/home.html"


class SearchPageView(TemplateView):
    template_name = "../templates/search.html"
