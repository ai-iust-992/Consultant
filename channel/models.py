import uuid

from django.db import models
from User.models import ConsultantProfile, BaseUser
from django.utils import timezone


class Channel(models.Model):
    subscribers = models.ManyToManyField(BaseUser, verbose_name="", through='channel.Subscription')
    consultant = models.OneToOneField(ConsultantProfile, verbose_name="channel owner", on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500, blank=True)
    invite_link = models.CharField(null=False, blank=False, max_length=32, unique=True)

    class Meta:
        verbose_name_plural = 'Channel'


class Subscription(models.Model):
    channel = models.ForeignKey(Channel, verbose_name="", on_delete=models.CASCADE)
    user = models.ForeignKey(BaseUser, verbose_name="", on_delete=models.DO_NOTHING)
    date_joined = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('channel', 'user',)
        verbose_name_plural = 'Subscription'
