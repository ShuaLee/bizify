from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('inventories', views.InventoryViewSet, basename='inventory')
router.register('items', views.ItemViewSet, basename='item')
router.register('item-details', views.ItemDetailViewSet,
                basename='item-detail')


app_name = 'inventory'
urlpatterns = router.urls
