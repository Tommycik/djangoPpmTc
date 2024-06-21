from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from recipes.models import Recipe


class Cook(models.Model):
    title = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    favourites = models.ManyToManyField(Recipe)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Cook.objects.create(title=instance)
