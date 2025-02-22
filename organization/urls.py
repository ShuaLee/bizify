from django.urls import path
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('profile', views.ProfileViewSet)
router.register('company', views.CompanyViewSet, basename='company')


urlpatterns = router.urls
