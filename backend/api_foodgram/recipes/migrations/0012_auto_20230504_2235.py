# Generated by Django 3.2 on 2023-05-04 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0011_alter_shopingcart_recipe'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='RecipesIngredients',
            new_name='RecipeIngredient',
        ),
        migrations.RenameModel(
            old_name='RecipesTags',
            new_name='RecipeTag',
        ),
        migrations.AddConstraint(
            model_name='favorites',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique_Favorites'),
        ),
        migrations.AddConstraint(
            model_name='recipeingredient',
            constraint=models.UniqueConstraint(fields=('recipe', 'ingredient'), name='unique_RecipeIngredient'),
        ),
        migrations.AddConstraint(
            model_name='recipetag',
            constraint=models.UniqueConstraint(fields=('recipe', 'tag'), name='unique_RecipeTags'),
        ),
        migrations.AddConstraint(
            model_name='shopingcart',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique_ShopingCart'),
        ),
        migrations.AddConstraint(
            model_name='subscribe',
            constraint=models.UniqueConstraint(fields=('user', 'following'), name='unique_Subscribe'),
        ),
    ]