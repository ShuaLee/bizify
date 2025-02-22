from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from .models import Profile, Company, Role, ProfileCompanyRole
from .serializers import ProfileSerializer, CompanySerializer

# Create your views here.


class ProfileViewSet(ListModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    # STILL NEED TO ADD AUTHENTICATION
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()


class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    # No permission_classes = [isAuthenticated] for now

    def perform_create(self, serializer):
        # Save the company, will be: company = serializer.save()
        company = serializer.save()

        admin_role, _ = Role.objects.get_or_create(
            company=company,
            name="Admin",
            defaults={'permissions': {"can_do_everything": True}}
        )
