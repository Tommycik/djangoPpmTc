from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages
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
    elements=[]
    # <a href={% url 'category_new' %}>New Category</a>
    # <a href={% url 'ingredient_new' %}>New Ingredient</a>
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
                    if any([cf.cleaned_data != {} for cf in formset1]) or any([cf.cleaned_data != {} for cf in formset2]):
                        if any([cf.cleaned_data != {} for cf in formset4]):
                            recipe.save()
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
                                                                           description=form2.cleaned_data['description'])

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
                            form.save_m2m()
                            return HttpResponseRedirect(recipe.get_absolute_url())
            if all([cf.is_valid() for cf in formset1]) and all([cf.is_valid() for cf in formset2]) :
                if all([cf.cleaned_data == {} for cf in formset1]) and all(
                        [cf.cleaned_data == {} for cf in formset2]):
                    messages.error(request, 'the recipe must have at least one ingredient.', extra_tags='ingredients')
            if all([cf.is_valid() for cf in formset4]):
                if all([cf.cleaned_data == {} for cf in formset4]) :
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
        formset1 = RecipeIngredientFormset(request.POST, prefix='ingredient')
        formset2 = NewIngredientFormset(request.POST, prefix='newingredient')
        formset3 = NewCategoryFormset(request.POST, prefix='category')
        formset4 = NewStepFormset(request.POST, prefix='step')
        ingredients_form = [RecipeIngredientListForm(request.POST, prefix=str(x) + "a", instance=ingredients[x]) for x in
                            range(0, ingredients.count())]
        steps_form = [RecipeStepListForm(request.POST, prefix=str(x) + "b", instance=steps[x]) for x in
                      range(0, steps.count())]

        # save the data from the form and
        # redirect to detail_view
        if form.is_valid() and all([cf.is_valid() for cf in ingredients_form]) and all(
                [cf.is_valid() for cf in steps_form]):
            if recipe.clean_rc(request.user):
                modified = form.save(commit=False)
                if all([cf.is_valid() for cf in formset1]) and all(
                    [cf.is_valid() for cf in formset2]) and all([cf.is_valid() for cf in formset3]) and all(
                    [cf.is_valid() for cf in formset4]):
                    if any([cf.cleaned_data != {} for cf in formset1]) or any(
                            [cf.cleaned_data != {} for cf in formset2]) or any([cf.cleaned_data != {} and not cf.cleaned_data["delete"] for cf in ingredients_form]):
                        if any([cf.cleaned_data != {} for cf in formset4]) or any([cf.cleaned_data != {} and not cf.cleaned_data["delete"] for cf in steps_form]):
                            recipe.save()
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
                                                                                 ingredient=form2.cleaned_data['ingredient'],
                                                                                 quantity=form2.cleaned_data['quantity'],
                                                                                 unit=form2.cleaned_data['unit'])

                                    ingredient.save()
                                    modified.ingredients.add(ingredient.ingredient)

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
                            recipe.save()
                            form.save_m2m()
                            return HttpResponseRedirect(recipe.get_absolute_url())
            if all([cf.is_valid() for cf in formset1]) and all([cf.is_valid() for cf in formset2]):
                if all([cf.cleaned_data == {} for cf in formset1]) and all(
                        [cf.cleaned_data == {} for cf in formset2]) and all([cf.cleaned_data == {} or cf.cleaned_data["delete"] for cf in ingredients_form]):
                    messages.error(request, 'the recipe must have at least one ingredient.', extra_tags='ingredients')
            if all([cf.is_valid() for cf in formset4]):
                if all([cf.cleaned_data == {} for cf in formset4]) and all([cf.cleaned_data == {} or cf.cleaned_data["delete"] for cf in steps_form]):
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
