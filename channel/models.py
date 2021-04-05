from django.db import models
from User.models import ConsultantProfile
class channel(models.Model):
    consultant = models.OneToOneField(ConsultantProfile, verbose_name="channal owner", on_delete=models.CASCADE) 
    name = models.CharField(max_length=50)
    description = models.CharField( max_length=500, blank=True)
    invite_link = models.CharField( max_length=250)
