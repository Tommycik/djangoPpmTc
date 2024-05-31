from django.urls import path
from . import views

urlpatterns = [
    path("input/", views.search_page_view, name="search"),
    path("", views.HomePageView.as_view(), name="home"),
]

