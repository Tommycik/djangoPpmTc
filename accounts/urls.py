from django.urls import path
from .views import (RecipeSignUpView, RecipeLoginView)

urlpatterns = [
    path("signup/", RecipeSignUpView.as_view(success_url="/accounts/login"), name="signup"),
    path("login/", RecipeLoginView.as_view(), name="login"),
    #path("signup/", SignUpView.as_view(), name="passwordChange"),
]
