from django.contrib import admin
from .models import Category
from .models import Recipe
from .models import Ingredient
# Register your models here.


admin.site.register(Category)
admin.site.register(Recipe)
admin.site.register(Ingredient)
