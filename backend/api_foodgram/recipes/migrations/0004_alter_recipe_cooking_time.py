# Generated by Django 3.2 on 2023-05-12 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20230512_2137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.DurationField(),
        ),
    ]
