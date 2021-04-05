from django.db import models
from django.utils import timezone
from channel.models import Channel
from User.models import UserProfile

class Message(models.Model):
    date =  models.DateTimeField( default = timezone.now)
    text = models.TextField( max_length=2000, blank=True, null=True)
    file_address = models.FileField( upload_to='files/message_file', blank=True, null=True)
    message_choice = [
        ('t', 'text'),
        ('i', 'image'),
        ('v', 'video'),
        ('a', 'audio'),
    ]
    message_type = models.CharField( max_length=1, choices=message_choice, default='t')
    class Meta:
        abstract=True

class ChannelMessage(Message):
    channel = models.ForeignKey( Channel, verbose_name="", on_delete=models.CASCADE)
    creator = models.ForeignKey( UserProfile, verbose_name="", on_delete=models.SET_NULL, null=True)