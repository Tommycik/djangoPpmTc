from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.forms import Textarea, TextInput
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView

from .forms import RecipeForm, RecipeIngredientFormset, NewCategoryFormset, NewIngredientFormset, \
    NewStepFormset, RecipeIngredientListForm, RecipeStepListForm
from .models import Recipe, Ingredient, Category, RecipeIngredient, RecipeStep


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
        context['title'] = "Recipes in the '" + Category.objects.get(pk=self.kwargs['pk']).title + "' category"
        return context


class RecipesIngredientPageView(RecentPageView):

    def get_queryset(self):
        queryset = Recipe.objects.all().filter(ingredients=self.kwargs['pk'])
        return queryset

    def get_context_data(self, **kwargs):
        context = super(RecentPageView, self).get_context_data(**kwargs)
        context['title'] = "Recipes that use '" + Ingredient.objects.get(pk=self.kwargs['pk']).title + ''
        return context


class CategoriesPageView(ListView):
    model = Category
    template_name = "../templates/subList.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['alphabet'] = map(chr, range(97, 123))
        context['numbers'] = range(0, 10)
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
        context['ingredients'] = RecipeIngredient.objects.filter(recipe=self.object.pk)
        context['categories'] = Category.objects.filter(pk__in=self.object.categories.all())
        context['steps'] = RecipeStep.objects.filter(recipe=self.object)
        return context


@login_required
def create_recipe_view(request):
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)
        formset1 = RecipeIngredientFormset(request.POST, prefix='ingredient')
        formset2 = NewIngredientFormset(request.POST, prefix='newingredient')
        formset3 = NewCategoryFormset(request.POST, prefix='category')
        formset4 = NewStepFormset(request.POST, prefix='step')

        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user

            if recipe.clean_rc(request.user):

                if all([cf.is_valid() for cf in formset1]) and all(
                        [cf.is_valid() for cf in formset2]) and all([cf.is_valid() for cf in formset3]) and all(
                        [cf.is_valid() for cf in formset4]):

                    if any([cf.cleaned_data != {} for cf in formset1]) or any(
                            [cf.cleaned_data != {} for cf in formset2]):

                        if any([cf.cleaned_data != {} for cf in formset4]):

                            recipe.save()
                            form.save_m2m()
                            for form2 in formset1:
                                if form2.cleaned_data != {}:
                                    ingredient = RecipeIngredient(recipe=recipe,
                                                                  ingredient=form2.cleaned_data['ingredient'],
                                                                  quantity=form2.cleaned_data['quantity'],
                                                                  unit=form2.cleaned_data['unit'])

                                    ingredient.save()
                                    recipe.ingredients.add(ingredient.ingredient)

                            for form2 in formset2:
                                if form2.cleaned_data != {}:
                                    ingredient = Ingredient.objects.create(title=form2.cleaned_data['ingredient'],
                                                                           description=form2.cleaned_data[
                                                                               'description'])

                                    ri = RecipeIngredient(recipe=recipe, ingredient=ingredient,
                                                          quantity=form2.cleaned_data['quantity'],
                                                          unit=form2.cleaned_data['unit'])
                                    ri.save()
                                    recipe.ingredients.add(ingredient)

                            for form2 in formset3:
                                if form2.cleaned_data != {}:
                                    child = form2.save(commit=True)
                                    recipe.categories.add(child)

                            for form2 in formset4:
                                if form2.cleaned_data != {}:
                                    step = RecipeStep(description=form2.cleaned_data['description'], recipe=recipe)
                                    step.save()

                            recipe.save()
                            return HttpResponseRedirect(recipe.get_absolute_url())

            if all([cf.is_valid() for cf in formset1]) and all([cf.is_valid() for cf in formset2]):
                if all([cf.cleaned_data == {} for cf in formset1]) and all(
                        [cf.cleaned_data == {} for cf in formset2]):

                    messages.error(request, 'the recipe must have at least one ingredient.', extra_tags='ingredients')

            if all([cf.is_valid() for cf in formset4]):
                if all([cf.cleaned_data == {} for cf in formset4]):

                    messages.error(request, 'the recipe must have at least one step.', extra_tags='steps')

            if not recipe.clean_rc(request.user):
                messages.error(request, 'this recipe already exists.', extra_tags='recipe')

    else:
        form = RecipeForm()
        formset1 = RecipeIngredientFormset(prefix='ingredient')
        formset2 = NewIngredientFormset(prefix='newingredient')
        formset3 = NewCategoryFormset(prefix='category')
        formset4 = NewStepFormset(prefix='step')

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
    name = "category"

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()

        form = super().get_form(form_class)
        form.fields['title'].widget = TextInput(attrs={'placeholder': 'Enter the name of the ' + self.name})
        form.fields['title'].help_text = "max 50 characters"
        form.fields['description'].widget = Textarea(attrs={'placeholder': 'Enter the description of the ' + self.name})
        form.fields['description'].help_text = "max 280 characters"
        return form

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
    name = "ingredient"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'New Ingredient'
        return context

    def get(self, request, *args, **kwargs):
        request.session['previous_page'] = request.META.get('HTTP_REFERER', self.default_redirect)
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return self.request.session['previous_page']


@login_required
def update_view(request, pk):
    recipe = get_object_or_404(Recipe, id=pk)

    if request.user != recipe.author:
        return redirect('access_denied')

    ingredients = RecipeIngredient.objects.filter(recipe=pk)
    steps = RecipeStep.objects.filter(recipe=pk)

    if request.method == 'POST':
        form = RecipeForm(request.POST or None, request.FILES, instance=recipe)
        formset1 = RecipeIngredientFormset(request.POST, prefix='ingredient')
        formset2 = NewIngredientFormset(request.POST, prefix='newingredient')
        formset3 = NewCategoryFormset(request.POST, prefix='category')
        formset4 = NewStepFormset(request.POST, prefix='step')
        ingredients_form = [RecipeIngredientListForm(request.POST, prefix=str(x) + "a", instance=ingredients[x]) for x
                            in
                            range(0, ingredients.count())]
        steps_form = [RecipeStepListForm(request.POST, prefix=str(x) + "b", instance=steps[x]) for x in
                      range(0, steps.count())]

        if form.is_valid() and all([cf.is_valid() for cf in ingredients_form]) and all(
                [cf.is_valid() for cf in steps_form]):

            if recipe.clean_rc(request.user):
                modified = form.save(commit=False)

                if all([cf.is_valid() for cf in formset1]) and all(
                        [cf.is_valid() for cf in formset2]) and all([cf.is_valid() for cf in formset3]) and all(
                        [cf.is_valid() for cf in formset4]):

                    if any([cf.cleaned_data != {} for cf in formset1]) or any(
                            [cf.cleaned_data != {} for cf in formset2]) or any(
                            [cf.cleaned_data != {} and not cf.cleaned_data["delete"] for cf in ingredients_form]):

                        if any([cf.cleaned_data != {} for cf in formset4]) or any(
                                [cf.cleaned_data != {} and not cf.cleaned_data["delete"] for cf in steps_form]):

                            modified.save()
                            form.save_m2m()
                            for cf in ingredients_form:
                                element = cf.save(commit=False)
                                if cf.cleaned_data["delete"]:
                                    element.delete()
                                else:
                                    element.save()

                            for cf in steps_form:
                                element = cf.save(commit=False)
                                if cf.cleaned_data["delete"]:
                                    element.delete()
                                else:
                                    element.save()

                            for form2 in formset1:
                                if form2.cleaned_data != {}:
                                    ingredient = RecipeIngredient.objects.create(recipe=modified,
                                                                                 ingredient=form2.cleaned_data[
                                                                                     'ingredient'],
                                                                                 quantity=form2.cleaned_data[
                                                                                     'quantity'],
                                                                                 unit=form2.cleaned_data['unit'])

                                    ingredient.save()
                                    modified.ingredients.add(ingredient.ingredient)

                            for form2 in formset2:
                                if form2.cleaned_data != {}:
                                    ingredient = Ingredient.objects.create(title=form2.cleaned_data['ingredient'],
                                                                           description=form2.cleaned_data[
                                                                               'description'])
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
                                    step = RecipeStep.objects.create(description=form2.cleaned_data['description'],
                                                                     recipe=modified)
                                    step.save()

                            modified.save()
                            return HttpResponseRedirect(recipe.get_absolute_url())

            if all([cf.is_valid() for cf in formset1]) and all([cf.is_valid() for cf in formset2]):

                if all([cf.cleaned_data == {} for cf in formset1]) and all(
                        [cf.cleaned_data == {} for cf in formset2]) and all(
                        [cf.cleaned_data == {} or cf.cleaned_data["delete"] for cf in ingredients_form]):

                    messages.error(request, 'the recipe must have at least one ingredient.', extra_tags='ingredients')

            if all([cf.is_valid() for cf in formset4]):

                if all([cf.cleaned_data == {} for cf in formset4]) and all(
                        [cf.cleaned_data == {} or cf.cleaned_data["delete"] for cf in steps_form]):

                    messages.error(request, 'the recipe must have at least one step.', extra_tags='steps')

            if not recipe.clean_rc(request.user):
                messages.error(request, 'this recipe already exists.', extra_tags='recipe')

    else:
        form = RecipeForm(instance=recipe)
        formset1 = RecipeIngredientFormset(prefix='ingredient')
        formset2 = NewIngredientFormset(prefix='newingredient')
        formset3 = NewCategoryFormset(prefix='category')
        formset4 = NewStepFormset(prefix='step')
        ingredients_form = [RecipeIngredientListForm(prefix=str(x) + "a", instance=ingredients[x]) for x in
                            range(0, ingredients.count())]
        steps_form = [RecipeStepListForm(prefix=str(x) + "b", instance=steps[x]) for x in
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


@login_required
def delete_view(request, pk):
    context = {}
    recipe = get_object_or_404(Recipe, id=pk)

    if request.user != recipe.author:
        return redirect('access_denied')

    if request.method == 'POST':

        if request.POST.get('confirm'):
            recipe.delete()
            return HttpResponseRedirect(reverse('recipe_yours'))

        next_page = request.POST.get('next', '/')
        return HttpResponseRedirect(next_page)

    context['title'] = "Delete recipe"
    context['object'] = 'This Recipe'
    return render(request, "../templates/delete.html", context)


class AuthorPageView(RecentPageView):
    def get_queryset(self):
        queryset = Recipe.objects.all().filter(author=User.objects.get(username=self.kwargs['name']).pk)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Recipes created by '" + self.kwargs['name'] + "'"
        return context


class BestPageView(RecentPageView):
    def get_queryset(self):
        queryset = Recipe.objects.all().order_by('-favourites')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Best Recipes"
        return context


class YourPageView(LoginRequiredMixin, AuthorPageView):
    def get_queryset(self):
        queryset = Recipe.objects.all().filter(author=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = (super(AuthorPageView, self).get_context_data(**kwargs))
        context['title'] = " Your Recipes"
        return context
