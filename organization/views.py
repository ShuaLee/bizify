from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from .models import Profile, Company, Role, ProfileCompanyRole
from .serializers import ProfileSerializer, CompanySerializer

# Create your views here.


class ProfileViewSet(ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    # Refine with AUTH later:
    # def get_queryset(self):
    #   return Profile.objects.filter(user=self.request.user)


class CompanyViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
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
