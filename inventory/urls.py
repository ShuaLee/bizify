from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'inventories', views.InventoryViewSet, basename='inventory')
router.register(r'items', views.ItemViewSet, basename='item')
router.register(r'attributes', views.AttributeViewSet, basename='attribute')
router.register(r'item-attributes', views.ItemAttributeViewSet,
                basename='item-attribute')

app_name = 'inventory'
urlpatterns = router.urls
