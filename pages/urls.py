from django.urls import path
from . import views

urlpatterns = [
    path('denied/', views.AccessDenied.as_view(), name='access_denied'),
    path("input/", views.search_page_view, name="search"),
    path("", views.HomePageView.as_view(), name="home"),
]

