from django.contrib import admin

from .models import Category, RecipeIngredient, RecipeStep
from .models import Recipe
from .models import Ingredient


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 0


class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline]


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Category)
admin.site.register(RecipeStep)
admin.site.register(Ingredient)
