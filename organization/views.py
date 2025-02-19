from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from .models import Company, Profile
from .serializers import CompanySerializer, ProfileSerializer

# Create your views here.


@api_view(['GET'])
def company_view(request, id):
    company = get_object_or_404(Company, pk=id)
    if request.method == 'GET':
        serializer = CompanySerializer(company)
        return Response(serializer.data)


@api_view(['GET'])
def profile_view(request, id):
    profile = get_object_or_404(Profile, pk=id)
    if request.method == 'GET':
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
def company_list(request, id):
    if request.method == 'GET':
        queryset = Company.objects.all()
        serializer = CompanySerializer(queryset, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CompanySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


"""
@api_view(['GET', 'PUT', 'DELETE'])
def company_description(request, id):
    company = get_object_or_404(Company, pk=id)
    if request.method == 'GET':
        serializer = CompanySerializer(company)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CompanySerializer(company, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        company.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
"""


class ProfileViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
