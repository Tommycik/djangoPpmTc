from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .forms import RecipeForm, RecipeIngredientForm, RecipeIngredientFormset
from .models import Recipe, Ingredient, Category, RecipeIngredient
from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView, DeleteView  # new


# Create your views here.


class RecentPageView(ListView):
    model = Recipe
    template_name = "../templates/list.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "New Recipes"
        return context


class RecipesCategoryPageView(RecentPageView):

    def get_queryset(self):
        queryset = Recipe.objects.all().filter(categories=self.kwargs['pk'])
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Recipes In The" + Category.objects.get(pk=self.kwargs['pk']).title + "Category"
        return context


class RecipesIngredientPageView(RecentPageView):

    def get_queryset(self):
        queryset = Recipe.objects.all().filter(ingredients=self.kwargs['pk'])
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Recipes That Use" + Category.objects.get(pk=self.kwargs['pk']).title
        return context


class CategoriesPageView(ListView):
    model = Category
    template_name = "../templates/subList.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['alphabet'] = map(chr, range(97, 123))
        context['title'] = "Categories"
        return context


class IngredientsPageView(CategoriesPageView):
    model = Ingredient

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Ingredients"
        return context


class DetailPageView(DetailView):
    model = Recipe
    template_name = "../templates/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ingredients'] = self.object.ingredients.all()
        return context


@login_required
def create_recipe_view(request):
    context = {}
    # <a href={% url 'category_new' %}>New Category</a>
    # <a href={% url 'ingredient_new' %}>New Ingredient</a>
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)

        if form.is_valid():

            recipe = form.save(commit=False)
            formset = RecipeIngredientFormset(request.POST, instance=recipe)
            recipe.author = request.user
            recipe.save()
            for form in formset:
                child = form.save(commit=False)
                recipe.ingredients.add(child)
                recipe.save()
            return HttpResponseRedirect(recipe.get_absolute_url())
    else:
        form = RecipeForm()
        recipe = Recipe()
        formset = RecipeIngredientFormset(instance=recipe)
        # formset2= RecipeCategoryFormset(instance=recipe)
        context = {
            'form': form,
            'formset': formset
        }
    return render(request, '../templates/create.html', context)


class CreateCategoryView(LoginRequiredMixin, CreateView):
    model = Category
    fields = ['title', 'description']
    template_name = "../templates/createSub.html"
    default_redirect = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'New Category'
        return context

    def get(self, request, *args, **kwargs):
        request.session['previous_page'] = request.META.get('HTTP_REFERER', self.default_redirect)
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return self.request.session['previous_page']


class CreateIngredientView(CreateCategoryView):
    model = Ingredient

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'New Ingredient'
        return context

    def get(self, request, *args, **kwargs):
        request.session['previous_page'] = request.META.get('HTTP_REFERER', self.default_redirect)
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return self.request.session['previous_page']


# class CreatePageView(LoginRequiredMixin, CreateView):
# model = Recipe
# fields = ['title', 'description', 'ingredients', 'time', 'body', 'image', 'categories']
# template_name = "../templates/create.html"

# def form_valid(self, form):

# c = form.cleaned_data["category"]
# i = form.cleaned_data["ingredient"]
# category = Category.objects.filter(name=c).first()
# ingredient = Ingredient.objects.filter(name=i).first()
# if not category:
#    category = Category.objects.create(name=c)
# if not ingredient:
#    category = Category.objects.create(name=c)
#     instance = form.save(commit=False)
# define the slug and any other programmatically generated fields
# instance.author = self.request.user
# instance.categories.add(category)
# instance.ingredients.add(ingredient)
#  instance.save()

#    return HttpResponseRedirect(instance.get_absolute_url()+"recipe/")


class ModifyPageView(LoginRequiredMixin, UpdateView):
    model = Recipe
    fields = ['title', 'description', 'ingredients', 'time', 'body', 'image', 'categories']
    template_name = "../templates/modify.html"

    def form_valid(self, form):
        instance = form.save()
        instance.save()

        return HttpResponseRedirect(instance.get_absolute_url() + "recipe/")


@login_required
def update_view(request, pk):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # fetch the object related to passed id
    recipe = get_object_or_404(Recipe, id=pk)
    ingredients = inlineformset_factory(Recipe, RecipeIngredient, min_num=1, exclude=("recipe",))
    if request.method == 'POST':
        # pass the object as instance in form
        form = RecipeForm(request.POST or None, instance=recipe)
        formset = ingredients(request.POST, request.FILES, instance=recipe)
        # save the data from the form and
        # redirect to detail_view
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return HttpResponseRedirect(recipe.get_absolute_url())

    else:

        form = RecipeForm(instance=recipe)
        formset = RecipeIngredientFormset(instance=recipe)

        context = {
            'form': form,
            'formset': formset
        }

    return render(request, "../templates/modify.html", context)


class DeletePageView(DeleteView):
    model = Recipe
    template_name = "../templates/delete.html"

    def get_success_url(self):
        return reverse('recipe_yours')


class AuthorPageView(RecentPageView):
    def get_queryset(self):
        queryset = Recipe.objects.all().filter(author=User.objects.get(username=self.kwargs['name']).pk)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.kwargs['name'] + " Recipes"
        return context


class YourPageView(LoginRequiredMixin, AuthorPageView):

    def get_queryset(self):
        queryset = Recipe.objects.all().filter(author=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = (super(AuthorPageView, self).get_context_data(**kwargs))
        context['title'] = " Your Recipes"
        return context
