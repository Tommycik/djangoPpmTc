from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from recipes.models import Recipe


# Create your models here.
class Cook(models.Model):
    title = models.OneToOneField(User, on_delete=models.CASCADE)
    favourites = models.ManyToManyField(Recipe)


# this method to generate Cook when User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Cook.objects.create(title=instance)

# this method to update profile when user is updated
#@receiver(post_save, sender=User)
#def save_user_profile(sender, instance, **kwargs):
# instance.favourites.save()
