from django import forms
from django.forms import ChoiceField


class SearchForm(forms.Form):
    FILTER_CHOICES = (
        ('all', 'All'),
        ('recipe', 'Recipe'),
        ('category', 'Category'),
        ('ingredient', 'Ingredient'),
        ('cook', 'Cook'),
    )

    filter_field = ChoiceField(choices=FILTER_CHOICES)
    search = forms.CharField(label="Search", max_length=110, widget=forms.TextInput(attrs={'placeholder': 'Type your '
                                                                                                          'search'}))