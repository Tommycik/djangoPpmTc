# Generated by Django 4.2.13 on 2024-06-18 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0014_alter_recipe_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipestep',
            name='description',
            field=models.TextField(max_length=300),
        ),
    ]