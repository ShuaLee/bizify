from django.conf import settings
from django.db import models

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True)
    country = models.CharField(max_length=30, blank=True)
    state = models.CharField(max_length=30, blank=True)
    city = models.CharField(max_length=30, blank=True)
    postal_code = models.CharField(max_length=15, blank=True)
    job_title = models.CharField(max_length=50, blank=True)

    # Magic methods
    def __str__(self):
        return self.user.email
