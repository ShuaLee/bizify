from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.


class Company(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='companies', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ['user__first_name', 'user__last_name']

    # Signal to automatically create a Profile when a User is created

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    # Magic methods
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
