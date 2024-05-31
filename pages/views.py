from django.http import request, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView
from django.views.generic import ListView, DetailView, FormView  # new

from accounts.models import Cook
from pages.forms import SearchForm
from recipes.models import Recipe, Category, Ingredient


# Create your views here.
class HomePageView(TemplateView):
    template_name = "../templates/home.html"


def SearchPageView(request):
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
            #return redirect("/search/results/", {"form": form})

        # if a GET (or any other method) we'll create a blank form
    else:
        form = SearchForm()

    return render(request, "../templates/search.html", {"form": form})


#def SearchResultsView(request,form):

   # return render(request, "../templates/SearchResults.html", {"results": results, "mode": form.fields["filter_field"]})


class earchResultsView(TemplateView):
    model = Recipe, Ingredient, Category, Cook
    template_name = "../templates/SearchResults.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipes = Recipe.objects.filter(tile__icontains=self.args['search'])
        categories = Category.objects.filter(tile__icontains=self.args['search'])
        ingredients = Ingredient.objects.filter(tile__icontains=self.kwargs['search'])
        cooks = Cook.objects.filter(tile__icontains=self.kwargs['search'])
        target = recipes
        # if self.kwargs['form'].filter_field == "recipe":
        #    categories.delete()
        # elif self.kwargs['form'].filter_field == "category":
        #    target = categories
        # elif self.kwargs['form'].filter_field == "ingredient":
        #    target = ingredients
        # elif self.kwargs['form'].filter_field == "cook":
        #    target = cooks
        context['mode'] = self.kwargs['mode']
        context['results'] = [recipes, categories, ingredients, cooks]

        return context
