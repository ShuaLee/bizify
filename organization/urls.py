from django.urls import path
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('company', views.CompanyViewSet)
router.register('profile', views.ProfileViewSet)

company_router = routers.NestedDefaultRouter(
    router, 'company', lookup='company')

urlpatterns = router.urls + company_router.urls
