from django.urls import path, include
from rest_framework_nested import routers
from . import views
from inventory import views as inventory_views

# Top-level router for organization resources
router = routers.DefaultRouter()
router.register(r'profile', views.ProfileViewSet, basename='profile')
router.register(r'company', views.CompanyViewSet, basename='company')

# Nested router for company-specific resources
company_router = routers.NestedDefaultRouter(
    router, r'company', lookup='company')
company_router.register(
    r'inventories', inventory_views.InventoryViewSet, basename='company-inventory')

app_name = 'organization'
urlpatterns = [
    path('', include(router.urls)),
    path('', include(company_router.urls))
]
