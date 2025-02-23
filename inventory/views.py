from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Inventory
from .serializers import InventorySerializer

# Create your views here.


class InventoryViewSet(ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
