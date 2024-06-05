from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("favourites/", views.FavouritesPageView.as_view(), name="recipe_favourites"),
    path("favourites/<int:pk>", views.favourite_add, name="recipe_favouriteAdd"),
    path("<int:pk>/user", views.DetailAccountView.as_view(), name="user_detail"),
    path("signup/", views.register, name="signup"),
    path("login/", views.Login, name="login"),

]
