from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Company
from .serializers import CompanySerializer

# Create your views here.


@api_view()
def company_list(request):
    queryset = Company.objects.all()
    serializer = CompanySerializer(queryset, many=True)
    return Response(serializer.data)


@api_view()
def company_description(request, id):
    company = get_object_or_404(Company, pk=id)
    serializer = CompanySerializer(company)
    return Response(serializer.data)
