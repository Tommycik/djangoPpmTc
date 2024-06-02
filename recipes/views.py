from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Recipe, Ingredient, Category
from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView, DeleteView  # new


# Create your views here.


class RecentPageView(ListView):
    model = Recipe
    template_name = "../templates/recent.html"
    paginate_by = 10


class RecipesCategoryPageView(ListView):
    model = Category
    template_name = "../templates/category.html"
    paginate_by = 10

    def get_queryset(self):
        queryset = Recipe.objects.all().filter(categories=self.kwargs['pk'])
        return queryset


class RecipesIngredientPageView(ListView):
    model = Ingredient
    template_name = "../templates/ingredient.html"
    paginate_by = 10

    def get_queryset(self):
        queryset = Recipe.objects.all().filter(ingredients=self.kwargs['pk'])
        return queryset


class CategoriesPageView(ListView):
    model = Category
    template_name = "../templates/categories.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['alphabet'] = map(chr, range(97, 123))
        return context


class IngredientsPageView(ListView):
    model = Ingredient
    template_name = "../templates/ingredients.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['alphabet'] = map(chr, range(97, 123))
        return context


class DetailPageView(DetailView):
    model = Recipe
    template_name = "../templates/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ingredients'] = self.object.ingredients.all()
        return context


class CreatePageView(LoginRequiredMixin, CreateView):
    model = Recipe
    fields = ['title', 'description', 'ingredients', 'time', 'body', 'image', 'categories']
    template_name = "../templates/create.html"

    def form_valid(self, form):

        c = form.cleaned_data["category"]
        i = form.cleaned_data["ingredient"]
        category = Category.objects.filter(name=c).first()
        ingredient = Ingredient.objects.filter(name=i).first()
        if not category:
            category = Category.objects.create(name=c)
        if not ingredient:
            category = Category.objects.create(name=c)
        instance = form.save(commit=False)
        # define the slug and any other programmatically generated fields
        instance.author = self.request.user
        instance.categories.add(category)
        instance.ingredients.add(ingredient)
        instance.save()

        return HttpResponseRedirect(instance.get_absolute_url()+"recipe/")


class ModifyPageView(LoginRequiredMixin, UpdateView):
    model = Recipe
    fields = ['title', 'description', 'ingredients', 'time', 'body', 'image', 'categories']
    template_name = "../templates/modify.html"

    def form_valid(self, form):
        instance = form.save()
        instance.save()

        return HttpResponseRedirect(instance.get_absolute_url()+"recipe/")


class DeletePageView(DeleteView):
    model = Recipe
    template_name = "../templates/delete.html"

    def get_success_url(self):
        return reverse('recipe_yours')


class AuthorPageView(ListView):
    model = Recipe
    template_name = "../templates/authorRecipes.html"
    paginate_by = 10

    def get_queryset(self):
        queryset = Recipe.objects.all().filter(author=User.objects.get(username=self.kwargs['name']).pk)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = self.kwargs['name']
        return context


class YoursPageView(LoginRequiredMixin, AuthorPageView):
    template_name = "../templates/userRecipes.html"

    def get_queryset(self):
        queryset = Recipe.objects.all().filter(author=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = (super(AuthorPageView, self).get_context_data(**kwargs))
        return context
