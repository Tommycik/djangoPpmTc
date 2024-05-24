from django.conf import settings
from django.db import models
from django.urls import reverse


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=255, primary_key=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    title = models.CharField(max_length=255, primary_key=True)

    def __str__(self):
        return self.title


class Recipe(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True, max_length=400)
    ingredients = models.ManyToManyField(Ingredient)
    time = models.IntegerField(default=0)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    image = models.ImageField(null=True)
    categories = models.ManyToManyField(Category)

    class Meta:
        db_table = "Recipes"
        ordering = ['-date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("recipe_detail", kwargs={"pk": self.pk})
