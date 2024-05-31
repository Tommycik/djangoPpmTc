from django.urls import path
from . import views

urlpatterns = [
    path("yours/", views.YoursPageView.as_view(), name="recipe_yours"),
    path("<str:name>/authorRecipes/", views.AuthorPageView.as_view(), name="recipe_author"),
    path("<int:pk>/delete/", views.DeletePageView.as_view(), name="recipe_delete"),
    path("<int:pk>/modify/", views.ModifyPageView.as_view(), name="recipe_modify"),
    path("create/", views.CreatePageView.as_view(), name="recipe_new"),
    path("<str:pk>/ingredient/", views.RecipesIngredientPageView.as_view(), name="recipes_ingredient"),
    path("<str:pk>/category/", views.RecipesCategoryPageView.as_view(), name="recipes_category"),
    path("<int:pk>/recipe", views.DetailPageView.as_view(), name="recipe_detail"),
    path("ingredient/", views.IngredientsPageView.as_view(), name="recipe_ingredients"),
    path("category/", views.CategoriesPageView.as_view(), name="recipe_categories"),
    path("", views.RecentPageView.as_view(), name="recent"),

]
