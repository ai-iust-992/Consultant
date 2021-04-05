from django.db import models
from User.models import ConsultantProfile
from User.models import UserProfile
from django.utils import timezone


class Channel(models.Model):
    subscribers = models.ManyToManyField( UserProfile, verbose_name="", through='Subscribtion')
    consultant = models.OneToOneField(ConsultantProfile, verbose_name="channal owner", on_delete=models.CASCADE) 
    name = models.CharField(max_length=50)
    description = models.CharField( max_length=500, blank=True)
    invite_link = models.CharField( max_length=250)

class Subscribtion(models.Model):
    channel = models.ForeignKey( Channel, verbose_name="", on_delete=models.CASCADE)
    user =  models.ForeignKey( UserProfile, verbose_name="", on_delete=models.CASCADE)
    date_joined = models.DateTimeField( default = timezone.now)
