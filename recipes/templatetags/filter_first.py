from django import template

from recipes.models import Category, Ingredient

register = template.Library()

@register.filter
def filter_first(list, char):
    if list.model == Category:
        return Category.objects.filter(title__startswith=char)
    elif list.model == Ingredient:
        return Ingredient.objects.filter(title__startswith=char)

