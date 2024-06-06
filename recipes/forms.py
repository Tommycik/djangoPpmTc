from django import forms
from django.contrib.admin.views import autocomplete
from django.forms import ChoiceField, inlineformset_factory, formset_factory

from recipes.models import Category, Recipe, Ingredient, RecipeIngredient, RecipeStep


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['categories', 'title', 'description', 'time', 'image']


class RecipeIngredientForm(forms.ModelForm):
    ingredient = forms.ModelChoiceField(
        queryset=Ingredient.objects.all(),

    )

    class Meta:
        Model = RecipeIngredient
        fields = ['quantity', 'unit']

    def __init__(self, *args, **kwargs):
        super(RecipeIngredientForm, self).__init__(*args, **kwargs)
        self.empty_permitted = False


class NewIngredientForm(forms.ModelForm):
    ingredient = forms.CharField(label='ingredient name', widget=forms.TextInput(), help_text="ingredient name")
    description = forms.CharField(label='ingredient description', widget=forms.TextInput(), help_text="ingredient"
                                                                                                      "description")

    class Meta:
        Model = RecipeIngredient
        fields = ['quantity', 'unit']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class StepForm(forms.ModelForm):
    class Meta:
        model = RecipeStep
        fields = ['description']


RecipeIngredientFormset = inlineformset_factory(Recipe,
                                                Recipe.ingredients.through,
                                                form=RecipeIngredientForm,
                                                extra=2,
                                                can_delete=False
                                                )

NewIngredientFormset = inlineformset_factory(Recipe,
                                             Recipe.ingredients.through,
                                             form=NewIngredientForm,
                                             extra=1,
                                             can_delete=False
                                             )

NewCategoryFormset = formset_factory(
    form=CategoryForm,
    extra=1,
    can_delete=False
)

NewStepFormset = formset_factory(
    form=StepForm,
    extra=1,
    can_delete=False
)
