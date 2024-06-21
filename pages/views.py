from django.shortcuts import render
from django.views.generic import TemplateView

from accounts.models import Cook
from pages.forms import SearchForm
from recipes.models import Recipe, Category, Ingredient


class HomePageView(TemplateView):
    template_name = "../templates/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home Page'
        return context


class AccessDenied(TemplateView):
    template_name = "../templates/refusedAccess.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Access Denied'
        return context


def search_page_view(request):
    if request.method == "POST":
        form = SearchForm(request.POST)

        if form.is_valid():
            search = form.cleaned_data["search"]
            recipes = Recipe.objects.filter(title__icontains=search)
            categories = Category.objects.filter(title__icontains=search)
            ingredients = Ingredient.objects.filter(title__icontains=search)
            cooks = Cook.objects.filter(title__id__icontains=search)
            results = [recipes, categories, ingredients, cooks]
            return render(request, "../templates/searchResults.html",
                          {"results": results, "mode": form.cleaned_data["filter_field"]})

    else:
        form = SearchForm()

    return render(request, "../templates/search.html", {"form": form})
