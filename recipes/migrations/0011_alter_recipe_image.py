# Generated by Django 4.2.13 on 2024-06-17 10:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('recipes', '0010_alter_recipe_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
