# Generated by Django 4.2.13 on 2024-05-28 22:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_ingredient_remove_recipe_ingredients_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['title']},
        ),
        migrations.AlterModelOptions(
            name='ingredient',
            options={'ordering': ['title']},
        ),
        migrations.AlterModelTable(
            name='category',
            table='Categories',
        ),
        migrations.AlterModelTable(
            name='ingredient',
            table='Ingredients',
        ),
    ]
