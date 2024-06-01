from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("favourites/", views.FavouritesPageView.as_view(), name="recipe_favourites"),
    path("favourites/<int:pk>", views.favourite_add, name="recipe_favouriteAdd"),
    path("signup/", views.RecipeSignUpView.as_view(success_url="/accounts/login"), name="signup"),
    path("login/", views.RecipeLoginView.as_view(), name="login"),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="registration/reset_password.html"),
         name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="registration"
                                                                                        "/password_reset_sent.html"),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_form.html"),
         name='password_reset_confirm'),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_done.html"),
         name='password_reset_complete')
]
