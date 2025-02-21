from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from .models import Profile
from .serializers import ProfileSerializer

# Create your views here.


class ProfileViewSet(ListModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    # STILL NEED TO ADD AUTHENTICATION
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
