# Generated by Django 4.2.13 on 2024-05-27 21:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_rename_user_cook_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cook',
            old_name='favorites',
            new_name='favourites',
        ),
    ]