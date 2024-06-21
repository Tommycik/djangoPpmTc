from django import template

from recipes.models import Category, Ingredient

register = template.Library()


@register.filter
def filter_first(objects, char):
    if objects.model == Category:
        return Category.objects.filter(title__startswith=char)
    elif objects.model == Ingredient:
        return Ingredient.objects.filter(title__startswith=char)
