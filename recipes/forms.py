from django import forms
from django.forms import ChoiceField, inlineformset_factory

from recipes.models import Category, Recipe, Ingredient, RecipeIngredient


class RecipeForm(forms.ModelForm):
    categories = forms.MultipleChoiceField(choices=Category.objects.all(), widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = Recipe
        fields = ['title', 'description', 'body', 'image', 'categories', 'ingredients']
        widgets = {
            'description': forms.Textarea(
                attrs={
                    'rows': 4,
                }
            ),
        }


class RecipeIngredientForm(forms.ModelForm):
    ingredient = forms.ModelChoiceField(
        queryset=Ingredient.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    cost = forms.CharField(required=False)

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
                                                can_delete=True
                                                )
