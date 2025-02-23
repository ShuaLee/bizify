from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Inventory, Item, ItemDetail
from .serializers import InventorySerializer, ItemSerializer, ItemDetailSerializer

# Create your views here.


class InventoryViewSet(ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer


class ItemViewSet(ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class ItemDetailViewSet(ModelViewSet):
    queryset = ItemDetail.objects.all()
    serializer_class = ItemDetailSerializer
