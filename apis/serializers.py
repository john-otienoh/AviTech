from rest_framework import serializers
from avibot.models import Aircraft

class AircraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aircraft
        fields = ['aircraft_name', 'slug', 'max_pax', 'purchase_price', 'hire_price_per_hour', 'aircraft_image_url']
