from django.urls import path
from .views import SignUpView

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("signup/", SignUpView.as_view(), name="login"),
    path("signup/", SignUpView.as_view(), name="logout"),
    path("signup/", SignUpView.as_view(), name="passwordChange"),
]
