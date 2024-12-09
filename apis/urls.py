from django.urls import path
from . import views

urlpatterns = [
    path('', views.AircraftListView.as_view(), name='aircraft_list'),
    path('<int:pk>/', views.AircraftDetailView.as_view(), name='aircraft_details')
]

