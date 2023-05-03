import csv
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Ingredient

CSV_DIR = Path(settings.BASE_DIR).parent.parent
print(CSV_DIR)


class Command(BaseCommand):
    help = 'Добавляет данные из файлов csv в базу данных'

    def handle(self, *args, **options):

        with open(
            f'{CSV_DIR}/data/ingredients.csv',
            'r',
            encoding='utf-8'
        ) as csv_file:
            r = csv.DictReader(csv_file)
            for row in r:
                try:
                    (Ingredient.objects.get_or_create(
                        name=row['name'], measurement_unit=row['units']))
                except Exception:
                    pass

            print('Done')
