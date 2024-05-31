
from django.shortcuts import render
from django.views.generic import TemplateView
from accounts.models import Cook
from pages.forms import SearchForm
from recipes.models import Recipe, Category, Ingredient


# Create your views here.
class HomePageView(TemplateView):
    template_name = "../templates/home.html"


def search_page_view(request):
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = SearchForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            search = form.cleaned_data["search"]
            recipes = Recipe.objects.filter(title__icontains=search)
            categories = Category.objects.filter(title__icontains=search)
            ingredients = Ingredient.objects.filter(title__icontains=search)
            cooks = Cook.objects.filter(title__id__icontains=search)
            results = [recipes, categories, ingredients, cooks]

            return render(request, "../templates/searchResults.html", {"results": results, "mode": form.cleaned_data["filter_field"]})

        # if a GET (or any other method) we'll create a blank form
    else:
        form = SearchForm()

    return render(request, "../templates/search.html", {"form": form})

