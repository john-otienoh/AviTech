from django.core.management.base import BaseCommand
import json
from avibot.models import Aircraft # Use absolute import

class Command(BaseCommand):
    help = 'Load JSON data into the database'

    def handle(self, *args, **kwargs):
        with open('data.json') as json_file:
            data = json.load(json_file)

        aircrafts = []
        for item in data:

            aircraft = Aircraft(
                aircraft_name=item['aircraft_name'],
                max_pax=item['max_pax'],
                purchase_price=item.get('purchase_price', 100000),
                hire_price_per_hour=item['hire_price_per_hour'],
                aircraft_image_url=item['aircraft_image_url'],
            )
            aircrafts.append(aircraft)

        Aircraft.objects.bulk_create(aircrafts)
        self.stdout.write(self.style.SUCCESS('Successfully loaded data'))