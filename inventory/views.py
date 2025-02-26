from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Inventory, Item, ItemDetail, InventorySetting
from .serializers import InventorySerializer, ItemSerializer, ItemDetailSerializer, InventorySettingSerializer

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


class InventorySettingViewSet(ModelViewSet):
    queryset = InventorySetting.objects.all()
    serializer_class = InventorySettingSerializer
