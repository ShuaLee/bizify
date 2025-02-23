from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('inventories', views.InventoryViewSet, basename='inventory')

app_name = 'inventory'
urlpatterns = router.urls
