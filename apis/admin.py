from django.contrib import admin
from .models import Aircraft

# Register your models here.
@admin.register(Aircraft)

class AircraftAdmin(admin.ModelAdmin):
    """Register Aircraft Model to the Admin panel"""
    list_display = ['name', 'slug', 'max_pax', 'purchase_price', 'hire_price_per_hour', 'aircraft_image_url']
    list_filter = ['max_pax', 'purchase_price', 'hire_price_per_hour',]
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    show_facets = admin.ShowFacets.ALWAYS
