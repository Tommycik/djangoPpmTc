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


class IngredientsPageView(ListView):
    model = Ingredient
    template_name = "../templates/ingredients.html"
    paginate_by = 10


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

    def get_success_url(self):
        return reverse('home')

    def form_valid(self, form):
        instance = form.save(commit=False)
        # define the slug and any other programmatically generated fields
        instance.author = self.request.user
        instance.save()

        return HttpResponseRedirect(self.get_success_url())


class ModifyPageView(LoginRequiredMixin, UpdateView):
    model = Recipe
    fields = ['title', 'description', 'ingredients', 'time', 'body', 'image', 'categories']
    template_name = "../templates/modify.html"

    def get_success_url(self):
        return reverse('home')


class DeletePageView(DeleteView):
    model = Recipe
    template_name = "../templates/delete.html"

    def get_success_url(self):
        return reverse('home')


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
        context = super().get_context_data(**kwargs)
        return context
