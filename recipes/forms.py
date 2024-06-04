from django import forms
from django.contrib.admin.views import autocomplete
from django.forms import ChoiceField, inlineformset_factory

from recipes.models import Category, Recipe, Ingredient, RecipeIngredient


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['categories', 'title', 'description', 'body', 'time', 'image']


class RecipeIngredientForm(forms.ModelForm):
    ingredient = forms.ModelChoiceField(
        queryset=Ingredient.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        Model = RecipeIngredient
        fields = ['ingredient', 'quantity', 'unit']
        widgets = {
            'quantity': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                }
            ),


        }


RecipeIngredientFormset = inlineformset_factory(Recipe,
                                                Recipe.ingredients.through,
                                                form=RecipeIngredientForm,
                                                extra=2,
                                                can_delete=False
                                                )
