from django.conf import settings
from django.db import models
from django.urls import reverse


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
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    image = models.ImageField(null=True, upload_to = "recipes/")
    categories = models.ManyToManyField(Category)

    class Meta:
        db_table = "Recipes"
        ordering = ['-date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("recipe_detail", kwargs={"pk": self.pk})

    def recipe_delete(self):
        return reverse("recipe_delete", kwargs={"pk": self.pk})

    def recipe_modify(self):
        return reverse("recipe_modify", kwargs={"pk": self.pk})


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, blank=True, null=True, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, blank=True, null=True, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=20, decimal_places=2)
    unit = models.CharField(
        choices=[('g', 'Gram(s)'), ('kg', 'Kilogram(s)'), ('l', 'Liter(s)'), ('cl', 'Centiliter(s)')], default='g',
        max_length=2)