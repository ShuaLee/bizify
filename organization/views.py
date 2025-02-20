from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from .models import Company, Profile
from .serializers import CompanySerializer, ProfileSerializer

# Create your views here.


class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def get_serializer_context(self):
        return {'request': self.request}


@api_view(['GET'])
def profile_view(request, id):
    profile = get_object_or_404(Profile, pk=id)
    if request.method == 'GET':
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)


class ProfileViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
