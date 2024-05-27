from django.urls import path
from . import views

urlpatterns = [
    path("favourites/", views.FavouritesPageView.as_view(), name="recipe_favourites"),
    path("yours/", views.YoursPageView.as_view(), name="recipe_yours"),
    path("<str:name>/authorRecipes/", views.AuthorPageView.as_view(), name="recipe_author"),
    path("<int:pk>/delete/", views.DeletePageView.as_view(), name="recipe_delete"),
    path("create/", views.CreatePageView.as_view(), name="recipe_new"),
    path("search/", views.SearchPageView.as_view(), name="search"),
    path("<int:pk>/", views.DetailPageView.as_view(), name="recipe_detail"),
    path("", views.RecentPageView.as_view(), name="recent"),

]