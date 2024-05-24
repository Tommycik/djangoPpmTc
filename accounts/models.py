from django.db import models
from django.contrib.auth.models import User

from recipes.models import Recipe


# Create your models here.
class Cook(models.Model):
    User = models.OneToOneField(User, on_delete=models.CASCADE)
    favorites = models.ManyToManyField(Recipe)
