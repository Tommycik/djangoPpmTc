from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .forms import RecipeForm, RecipeIngredientForm, RecipeIngredientFormset, NewCategoryFormset, NewIngredientFormset, \
    NewStepFormset, StepForm, RecipeIngredientListForm, RecipeStepListForm
from .models import Recipe, Ingredient, Category, RecipeIngredient, RecipeStep
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
        context = super(RecentPageView, self).get_context_data(**kwargs)
        context['title'] = "Recipes In The" + Category.objects.get(pk=self.kwargs['pk']).title + "Category"
        return context


class RecipesIngredientPageView(RecentPageView):

    def get_queryset(self):
        queryset = Recipe.objects.all().filter(ingredients=self.kwargs['pk'])
        return queryset

    def get_context_data(self, **kwargs):
        context = super(RecentPageView, self).get_context_data(**kwargs)
        context['title'] = "Recipes That Use" + Ingredient.objects.get(pk=self.kwargs['pk']).title
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
        context = super(CategoriesPageView, self).get_context_data(**kwargs)
        context['title'] = "Ingredients"
        return context


class DetailPageView(DetailView):
    model = Recipe
    template_name = "../templates/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ingredients'] = RecipeIngredient.objects.filter(recipe=self.object.pk)
        context['categories'] = Category.objects.filter(pk__in=self.object.categories.all())
        context['steps'] = RecipeStep.objects.filter(recipe=self.object)
        return context


@login_required
def create_recipe_view(request):
    context = {}
    # <a href={% url 'category_new' %}>New Category</a>
    # <a href={% url 'ingredient_new' %}>New Ingredient</a>
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)
        formset1 = RecipeIngredientFormset(request.POST)
        formset2 = NewIngredientFormset(request.POST)
        formset3 = NewCategoryFormset(request.POST)
        formset4 = NewStepFormset(request.POST)
        if form.is_valid():

            recipe = form.save(commit=False)
            if all([cf.is_valid() for cf in formset1]) and all(
                    [cf.is_valid() for cf in formset2]) and all([cf.is_valid() for cf in formset3]) and all(
                [cf.is_valid() for cf in formset4]):
                recipe.author = request.user
                recipe.save()
                form.save_m2m()
                for form2 in formset1:
                    if form2.cleaned_data != {}:
                        ingredient = RecipeIngredient.objects.create(recipe=recipe,
                                                                     ingredient=form2.cleaned_data['ingredient'],
                                                                     quantity=form2.cleaned_data['quantity'],
                                                                     unit=form2.cleaned_data['unit'])

                        ingredient.save()
                        recipe.ingredients.add(form2.cleaned_data['ingredient'])
                        recipe.save()

                for form2 in formset2:
                    if form2.cleaned_data != {}:
                        ingredient = Ingredient.objects.create(title=form2.cleaned_data['ingredient'],
                                                               description=form2.cleaned_data['description'])
                        ingredient.save()
                        ri = RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient,
                                                             quantity=form2.cleaned_data['quantity'],
                                                             unit=form2.cleaned_data['unit'])
                        ri.save()
                        recipe.ingredients.add(ingredient)
                        recipe.save()

                for form2 in formset3:
                    if form2.cleaned_data != {}:
                        child = form2.save(commit=True)
                        recipe.categories.add(child)
                        recipe.save()

                for form2 in formset4:
                    if form2.cleaned_data != {}:
                        step = RecipeStep.objects.create(description=form2.cleaned_data['description'], recipe=recipe)
                        step.save()
                return HttpResponseRedirect(recipe.get_absolute_url())
    else:
        form = RecipeForm()
        recipe = Recipe()
        formset1 = RecipeIngredientFormset()
        formset2 = NewIngredientFormset()
        formset3 = NewCategoryFormset()
        formset4 = NewStepFormset()

    context = {
        'form': form,
        'formset1': formset1,
        'formset2': formset2,
        'formset3': formset3,
        'formset4': formset4
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

@login_required
def update_view(request, pk):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # fetch the object related to passed id
    recipe = get_object_or_404(Recipe, id=pk)
    ingredients = RecipeIngredient.objects.filter(recipe=pk)
    steps = RecipeStep.objects.filter(recipe=pk)
    if request.method == 'POST':
        # pass the object as instance in form
        form = RecipeForm(request.POST or None, instance=recipe)
        formset1 = RecipeIngredientFormset(request.POST)
        formset2 = NewIngredientFormset(request.POST)
        formset3 = NewCategoryFormset(request.POST)
        formset4 = NewStepFormset(request.POST)
        ingredients_form = [RecipeIngredientListForm(request.POST, prefix=str(x), instance=ingredients[x]) for x in
                            range(0, ingredients.count())]
        steps_form = [RecipeStepListForm(request.POST, prefix=str(x), instance=steps[x]) for x in
                      range(0, steps.count())]

        # save the data from the form and
        # redirect to detail_view
        if form.is_valid() and all([cf.is_valid() for cf in ingredients_form]) and all(
                [cf.is_valid() for cf in steps_form]):
            modified = form.save(commit=False)
            if all([cf.is_valid() for cf in formset1]) and all(
                [cf.is_valid() for cf in formset2]) and all([cf.is_valid() for cf in formset3]) and all(
                [cf.is_valid() for cf in formset4]):
                for cf in ingredients_form:
                    element = cf.save(commit=False)
                    if cf.cleaned_data["delete"]:
                        element.delete()
                    else:
                        element = cf.save()

                for cf in steps_form:
                    element = cf.save(commit=False)
                    if cf.cleaned_data["delete"]:
                        element.delete()
                    else:
                        element.save()


                for form2 in formset1:
                    if form2.cleaned_data != {}:
                        ingredient = RecipeIngredient.objects.create(recipe=modified,
                                                                     ingredient=form2.cleaned_data['ingredient'],
                                                                     quantity=form2.cleaned_data['quantity'],
                                                                     unit=form2.cleaned_data['unit'])

                        ingredient.save()
                        modified.ingredients.add(form2.cleaned_data['ingredient'])

                for form2 in formset2:
                    if form2.cleaned_data != {}:
                        ingredient = Ingredient.objects.create(title=form2.cleaned_data['ingredient'],
                                                               description=form2.cleaned_data['description'])
                        ingredient.save()
                        ri = RecipeIngredient.objects.create(recipe=modified, ingredient=ingredient,
                                                             quantity=form2.cleaned_data['quantity'],
                                                             unit=form2.cleaned_data['unit'])
                        ri.save()
                        modified.ingredients.add(ingredient)

                for form2 in formset3:
                    if form2.cleaned_data != {}:
                        child = form2.save(commit=True)
                        modified.categories.add(child)

                for form2 in formset4:
                    if form2.cleaned_data != {}:
                        step = RecipeStep.objects.create(description=form2.cleaned_data['description'], recipe=modified)
                        step.save()

                if modified.clean():
                    modified.save()
                    return HttpResponseRedirect(recipe.get_absolute_url())

    else:

        form = RecipeForm(instance=recipe)
        formset1 = RecipeIngredientFormset()
        formset2 = NewIngredientFormset()
        formset3 = NewCategoryFormset()
        formset4 = NewStepFormset()
        ingredients_form = [RecipeIngredientListForm(prefix=str(x), instance=ingredients[x]) for x in
                            range(0, ingredients.count())]
        steps_form = [RecipeStepListForm(prefix=str(x), instance=steps[x]) for x in
                      range(0, steps.count())]

    context = {
        'form': form,
        'ingredients': ingredients_form,
        'steps': steps_form,
        'formset1': formset1,
        'formset2': formset2,
        'formset3': formset3,
        'formset4': formset4
    }

    return render(request, "../templates/modify.html", context)


class DeletePageView(LoginRequiredMixin, DeleteView):
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
