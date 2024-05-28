from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView

from accounts.models import Cook
from .models import Recipe
from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView, DeleteView  # new


# Create your views here.


class RecentPageView(ListView):
    model = Recipe
    template_name = "../templates/recent.html"
    paginate_by = 10


class DetailPageView(DetailView):
    model = Recipe
    template_name = "../templates/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ingredients'] = self.object.ingredients.all()
        return context


class SearchPageView(ListView):
    model = Recipe
    template_name = "../templates/recent.html"


class CreatePageView(CreateView):
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


class ModifyPageView(UpdateView):
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


class YoursPageView(ListView):
    model = Recipe
    template_name = "../templates/userRecipes.html"
    paginate_by = 10

    def get_queryset(self):
        queryset = Recipe.objects.all().filter(author=self.request.user)
        return queryset


class FavouritesPageView(YoursPageView):
    template_name = "../templates/favourites.html"

    def get_queryset(self):
        queryset = Recipe.objects.filter(title__in=(Cook.objects.get(title=self.request.user).favourites.all()))
        return queryset


class AuthorPageView(YoursPageView):
    template_name = "../templates/authorRecipes.html"

    def get_queryset(self):
        queryset = Recipe.objects.all().filter(author=User.objects.get(username=self.kwargs['name']).pk)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = self.kwargs['name']
        return context


def favourite_add(request, pk):
    favourite = Cook.objects.get(title=request.user)
    favourite.favourites.add(pk)
    #favourite.save()
    return HttpResponseRedirect(reverse('home'))
