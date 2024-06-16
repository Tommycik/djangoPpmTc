from _decimal import Decimal
from django.conf import settings
from django.contrib.postgres import serializers
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q
from django.urls import reverse

from accounts import forms


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=255, primary_key=True)
    description = models.TextField()

    class Meta:
        db_table = "Categories"
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("recipes_category", kwargs={"pk": self.pk})


class Ingredient(models.Model):
    title = models.CharField(max_length=255, primary_key=True)
    description = models.TextField(blank=True)

    class Meta:
        db_table = "Ingredients"
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("recipes_ingredient", kwargs={"pk": self.pk})


class Recipe(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True, max_length=400)
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')
    time = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    image = models.ImageField(null=True, upload_to="recipes/")
    categories = models.ManyToManyField(Category, blank=True)

    class Meta:
        db_table = "Recipes"
        ordering = ['-date']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'], name='unique_migration_host_combination'
            )
        ]

    def clean_rc(self,user):
        recipe = Recipe.objects.filter(title=self.title, author=user)
        if recipe.exists() and recipe.filter(~Q(id=self.pk)).exists():
            return False
        else:
            return True

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("recipe_detail", kwargs={"pk": self.pk})

    def recipe_delete(self):
        return reverse("recipe_delete", kwargs={"pk": self.pk})

    def recipe_modify(self):
        return reverse("recipe_modify", kwargs={"pk": self.pk})


class RecipeStep(models.Model):
    description = models.TextField()
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, blank=True, null=True, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, blank=True, null=True, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=20, validators=[MinValueValidator(Decimal('0.01'))], decimal_places=2)
    unit = models.CharField(
        choices=[('g', 'Gram(s)'), ('kg', 'Kilogram(s)'), ('l', 'Liter(s)'), ('cl', 'Centiliter(s)')],
        max_length=2)
