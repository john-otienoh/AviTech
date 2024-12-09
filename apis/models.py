from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify


# Create your models here.
class Aircraft(models.Model):
    """Stores our Aircraft Details"""
    name = models.CharField(max_length=30)
    slug = models.SlugField()
    max_pax = models.IntegerField()
    purchase_price = models.IntegerField()
    hire_price_per_hour = models.IntegerField()
    aircraft_image_url = models.URLField()

    def save(self, *args, **kwargs):
        """Automatically generate slug from name"""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs) 

    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse(
    #         'mente:bookmark_detail',
    #         args=[
    #             self.slug,
    #         ],
    #     )
    
    def __str__(self):
        return self.name
    