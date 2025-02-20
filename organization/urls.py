from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register('company', views.CompanyViewSet)
router.register('profile', views.ProfileViewSet)

urlpatterns = router.urls
