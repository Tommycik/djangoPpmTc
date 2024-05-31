from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    #path("results/<str:somevar>/ ", views.SearchResultsView, name="search_results"),
    path("input/", views.SearchPageView, name="search"),
    path("", views.HomePageView.as_view(), name="home"),
]

