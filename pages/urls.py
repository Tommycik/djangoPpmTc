from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("input/", views.SearchPageView.as_view(), name="search"),
    path("", views.HomePageView.as_view(), name="home"),
]

