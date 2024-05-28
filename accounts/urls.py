from django.urls import path
from . import views

urlpatterns = [
    path("favourites/", views.FavouritesPageView.as_view(), name="recipe_favourites"),
    path("favourites/<int:pk>", views.favourite_add, name="recipe_favouriteAdd"),
    path("signup/", views.RecipeSignUpView.as_view(success_url="/accounts/login"), name="signup"),
    path("login/", views.RecipeLoginView.as_view(), name="login"),
    #path("signup/", SignUpView.as_view(), name="passwordChange"),
]
