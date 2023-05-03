# Generated by Django 3.2 on 2023-04-23 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(max_length=116, unique=True),
        ),
        migrations.AlterField(
            model_name='recipesingredients',
            name='units',
            field=models.CharField(choices=[('GRAMS', 'гр'), ('MILLILITERS', 'мл'), ('PIECES', 'шт.'), ('BIGSPOON', 'ст. л.'), ('TEASPOON', 'ч. л.'), ('NOTHING', ' ')], max_length=11, verbose_name='единицы измерения'),
        ),
    ]
