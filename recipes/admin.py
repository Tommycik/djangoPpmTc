from django.contrib import admin
from .models import Category
from .models import Recipe
from .models import Ingredient
# Register your models here.

class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra=0

class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline]

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Category)
admin.site.register(Ingredient)
