from django.urls import path

from . import views

urlpatterns = [
    path("search", views.SearchPageView.as_view(), name="search"),
    path("<int:pk>/", views.DetailPageView.as_view(), name="recipe_detail"),
    path("", views.RecentPageView.as_view(), name="recent"),

]