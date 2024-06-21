from django import forms
from django.forms import formset_factory

from recipes.models import Category, Recipe, Ingredient, RecipeIngredient, RecipeStep


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['categories', 'title', 'description', 'time', 'image']
        help_texts = {
            'title': 'You can use max 100 characters',
            'description': 'You can use max 280 characters',
            'time': 'time in minutes',
        }
        widgets = {
            'title': forms.Textarea(attrs={'placeholder': 'Enter the name of the recipe'}),
            'description': forms.Textarea(attrs={'placeholder': 'Enter the description of the recipe'}),
        }


class RecipeIngredientForm(forms.ModelForm):
    ingredient = forms.ModelChoiceField(
        queryset=Ingredient.objects.all(),
    )
    quantity = forms.DecimalField()
    unit = forms.ChoiceField(
        choices=[('', '----'), ('g', 'Gram(s)'), ('kg', 'Kilogram(s)'), ('l', 'Liter(s)'), ('cl', 'Centiliter(s)')],
    )

    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'quantity', 'unit']


class RecipeIngredientListForm(RecipeIngredientForm):
    delete = forms.BooleanField(required=False, help_text='Delete this ingredient from the recipe?')


class NewIngredientForm(forms.ModelForm):
    ingredient = forms.CharField(label='Ingredient', widget=forms.TextInput(attrs={'placeholder': 'Name of the new '
                                                                                                  'ingredient'}),
                                 help_text='You can use max 50'
                                           'characters')
    description = forms.CharField(label='ingredient description',
                                  widget=forms.TextInput(attrs={'placeholder': 'Description of the'
                                                                               ' ingredient'}), help_text='You can use '
                                                                                                          'max 280 '
                                                                                                          'characters')

    class Meta:
        model = RecipeIngredient
        fields = ['quantity', 'unit']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title', 'description']
        help_texts = {
            'title': 'You can use max 50 characters',
            'description': 'You can use max 280 characters',
        }
        widgets = {
            'title': forms.Textarea(attrs={'placeholder': 'Enter the name of the new category'}),
            'description': forms.Textarea(attrs={'placeholder': 'Enter the description of the new category'}),
        }


class StepForm(forms.ModelForm):
    class Meta:
        model = RecipeStep
        fields = ['description']
        help_texts = {
            'description': 'You can use max 300 characters',
        }
        widgets = {
            'description': forms.Textarea(attrs={'placeholder': 'Describe how this step works'}),
        }


class RecipeStepListForm(StepForm):
    delete = forms.BooleanField(required=False, help_text='Delete this step from the recipe?')


RecipeIngredientFormset = formset_factory(form=RecipeIngredientForm,
                                          extra=1,
                                          can_delete=False
                                          )

NewIngredientFormset = formset_factory(form=NewIngredientForm,
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
