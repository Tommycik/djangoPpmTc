# Generated by Django 4.2.13 on 2024-06-12 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_remove_recipe_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='categories',
            field=models.ManyToManyField(blank=True, to='recipes.category'),
        ),
    ]