from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True)
    country = models.CharField(max_length=30, blank=True)
    state = models.CharField(max_length=30, blank=True)
    city = models.CharField(max_length=30, blank=True)
    postal_code = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=100, blank=True)

    # Magic methods
    def __str__(self):
        return self.user.email

    # Signal to automatically create a Profile when a User is created

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
