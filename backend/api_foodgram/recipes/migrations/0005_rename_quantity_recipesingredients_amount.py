# Generated by Django 3.2 on 2023-04-27 14:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_auto_20230427_1544'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipesingredients',
            old_name='quantity',
            new_name='amount',
        ),
    ]
