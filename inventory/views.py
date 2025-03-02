from rest_framework.viewsets import ModelViewSet
from .models import Inventory, Item, Attribute, ItemAttribute
from .serializers import InventorySerializer, ItemSerializer, AttributeSerializer, ItemAttributeSerializer


class InventoryViewSet(ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer


class ItemViewSet(ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class AttributeViewSet(ModelViewSet):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer


class ItemAttributeViewSet(ModelViewSet):
    queryset = ItemAttribute.objects.all()
    serializer_class = ItemAttributeSerializer
