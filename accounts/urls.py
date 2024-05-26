from django.urls import path
from .views import (RecipeSignUpView, RecipeLoginView)
#RecipeLogOutView,
#class RecipeLogOutView(LogoutView):
  #  form_class = UserCreationForm
    #success_url = "home"
    #template_name = "registration/logOut.html"
urlpatterns = [
    path("signup/", RecipeSignUpView.as_view(success_url="/accounts/login"), name="signup"),
    path("login/", RecipeLoginView.as_view(), name="login"),
    #path("logout/", RecipeLogOutView.as_view(), name="logout"),
    #path("signup/", SignUpView.as_view(), name="passwordChange"),
]
