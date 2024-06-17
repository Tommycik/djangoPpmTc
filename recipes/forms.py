from django import forms
from django.forms import formset_factory
from recipes.models import Category, Recipe, Ingredient, RecipeIngredient, RecipeStep


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['categories', 'title', 'description', 'time', 'image']


class RecipeIngredientForm(forms.ModelForm):
    ingredient = forms.ModelChoiceField(
        queryset=Ingredient.objects.all(),

    )
    quantity = forms.DecimalField()
    unit = forms.ChoiceField(
        choices=[('', '----'),('g', 'Gram(s)'), ('kg', 'Kilogram(s)'), ('l', 'Liter(s)'), ('cl', 'Centiliter(s)')],
    )

    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'quantity', 'unit']


class RecipeIngredientListForm(RecipeIngredientForm):
    delete = forms.BooleanField(required=False, help_text='delete ingredient from the recipe?')


class NewIngredientForm(forms.ModelForm):
    ingredient = forms.CharField(label='ingredient name', widget=forms.TextInput(), help_text="ingredient name")
    description = forms.CharField(label='ingredient description', widget=forms.TextInput(), help_text="ingredient"
                                                                                                      "description")

    class Meta:
        model = RecipeIngredient
        fields = ['quantity', 'unit']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class StepForm(forms.ModelForm):
    class Meta:
        model = RecipeStep
        fields = ['description']


class RecipeStepListForm(StepForm):
    delete = forms.BooleanField(required=False, help_text='delete step from the recipe?')


RecipeIngredientFormset = formset_factory(form=RecipeIngredientForm,
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
