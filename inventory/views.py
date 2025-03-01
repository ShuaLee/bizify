from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Inventory, Item, ItemDetail, InventorySetting
from .serializers import InventorySerializer, ItemSerializer, ItemDetailSerializer, InventorySettingSerializer

# Create your views here.


class InventoryViewSet(ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer


class ItemViewSet(ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = {'details__setting__key': [
        'exact'], 'details__value': ['exact', 'gt', 'lt', 'contains']}
    ordering_fields = ['details__value', 'name', 'quantity']


class ItemDetailViewSet(ModelViewSet):
    queryset = ItemDetail.objects.all()
    serializer_class = ItemDetailSerializer


class InventorySettingViewSet(ModelViewSet):
    queryset = InventorySetting.objects.all()
    serializer_class = InventorySettingSerializer
