from django.urls import path
from . import views

app_name = 'avibot'

urlpatterns = [
    path('', views.home, name='home'),
]
