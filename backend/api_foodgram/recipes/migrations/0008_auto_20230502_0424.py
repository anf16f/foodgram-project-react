# Generated by Django 3.2 on 2023-05-02 01:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0007_rename_units_ingredient_measurement_unit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipesingredients',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredients', to='recipes.ingredient'),
        ),
        migrations.AlterField(
            model_name='recipesingredients',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='in_recipes', to='recipes.recipe'),
        ),
        migrations.AlterField(
            model_name='recipestags',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='on_recipes', to='recipes.recipe'),
        ),
        migrations.AlterField(
            model_name='recipestags',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='recipes.tag'),
        ),
    ]
