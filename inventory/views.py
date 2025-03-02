from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, CharFilter
from .models import Inventory, Item
from .serializers import InventorySerializer, ItemSerializer

# Create your views here.


class ItemFilter(FilterSet):
    # Custom filter for JSONField keys
    details = CharFilter(method='filter_details')

    def filter_details(self, queryset, name, value):
        # Expect query param like ?details=part_no:ABC123
        if ':' in value:
            key, val = value.split(':', 1)
            return queryset.filter(**{f'details__{key}': val})
        return queryset

    class Meta:
        model = Item
        fields = ['inventory', 'name', 'quantity']  # Direct fields


class InventoryViewSet(ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer


class ItemViewSet(ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ItemFilter  # Use custom filter
    # Limited to direct fields for simplicity
    ordering_fields = ['name', 'quantity']
