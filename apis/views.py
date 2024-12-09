from rest_framework import generics
from .serializers import AircraftSerializer
from avibot.models import Aircraft

# Create your views here.
class AircraftListView(generics.ListAPIView):
    queryset = Aircraft.objects.all()
    serializer_class = AircraftSerializer

class AircraftDetailView(generics.RetrieveAPIView):
    queryset = Aircraft.objects.all()
    serializer_class = AircraftSerializer

