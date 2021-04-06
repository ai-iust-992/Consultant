import uuid

from django.db import models
from User.models import ConsultantProfile
from User.models import UserProfile
from django.utils import timezone


class Channel(models.Model):
    subscribers = models.ManyToManyField(UserProfile, verbose_name="", through='channel.Subscription')
    consultant = models.OneToOneField(ConsultantProfile, verbose_name="channel owner", on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500, blank=True)
    invite_link = models.CharField(null=False, blank=False, max_length=32, unique=True)

    class Meta:
        verbose_name_plural = 'Channel'


class Subscription(models.Model):
    channel = models.ForeignKey(Channel, verbose_name="", on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, verbose_name="", on_delete=models.CASCADE)
    date_joined = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = 'Subscription'
