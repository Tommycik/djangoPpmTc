from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from recipes.views import YoursPageView
from .models import Cook
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView


# Create your views here.
class RecipeSignUpView(CreateView):
    form_class = UserCreationForm
    template_name = "registration/signup.html"


class RecipeLoginView(LoginView):
    template_name = "registration/login.html"

    def get(self, request, *args, **kwargs):
        request.session['previous_page'] = request.META.get('HTTP_REFERER', self.success_url)
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        control = self.request.session['previous_page']
        check = self.request.build_absolute_uri(reverse_lazy("signup"))
        if control == check:
            return reverse_lazy("home")
        else:
            return self.request.session['previous_page']


class FavouritesPageView(YoursPageView):
    template_name = "../templates/favourites.html"

    def get_queryset(self):
        queryset = Cook.objects.get(title=self.request.user).favourites.all()
        return queryset


@login_required
def favourite_add(request, pk):
    cook = Cook.objects.get(title=request.user)
    favourites=cook.favourites.all()
    if favourites.filter(pk=pk).exists():
        cook.favourites.remove(pk)
    else:
        cook.favourites.add(pk)
    return HttpResponseRedirect(reverse('home'))



