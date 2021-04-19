from django.utils import timezone

from django.db import models
from django.contrib.auth.models import AbstractUser


def validate_phone_number(value):
    from django.core.exceptions import ValidationError
    # check phone number regex and return ValidationError
    pass


def validate_avatar_extension(value):
    import os
    from django.core.exceptions import ValidationError
    extension = os.path.splitext(value.name)[1]
    valid_extensions = ['.jpg', '.png']
    if extension.lower() not in valid_extensions:
        raise ValidationError('Unsupported file extension')


class BaseUser(AbstractUser):
    email = models.EmailField(null=False, blank=False, unique=True)
    phone_number = models.CharField(max_length=11, null=False, blank=False, unique=True,
                                    validators=[validate_phone_number])
    avatar = models.FileField(upload_to="files/user_avatar", null=True, blank=True,
                              validators=[validate_avatar_extension])
    user_type_choices = [
        ('Lawyer', 'Lawyer'),
        ('normal_user', 'normal_user'),
        ('medical', 'medical'),
        ('Entrance_Exam', 'Entrance_Exam'),
        ('Psychology', 'Psychology'),
        ('Educationalـimmigration', 'Educationalـimmigration'),
        ('Academicـadvice', 'Academicـadvice')
    ]
    user_type = models.CharField(null=False, blank=False, choices=user_type_choices, default="normal_user",
                                 max_length=32)


class UserProfile(BaseUser):
    private_profile = models.BooleanField(default=False, null=False, blank=False)

    class Meta:
        verbose_name_plural = 'UserProfile'


class ConsultantProfile(BaseUser):
    private_profile = models.BooleanField(default=False, null=False, blank=False)
    accepted = models.BooleanField(default=False, null=False, blank=False)
    my_secretaries = models.ManyToManyField(
        UserProfile,
    )
    certificate = models.FileField(upload_to="files/lawyers/certificate", null=True, blank=True)

    class Meta:
        verbose_name_plural = 'ConsultantProfile'


class Request(models.Model):
    target_user = models.ForeignKey(BaseUser, verbose_name="target user", on_delete=models.CASCADE)
    request_text = models.CharField(null=True, blank=True, max_length=2000)
    answer_text = models.CharField(null=True, blank=True, max_length=2000)
    request_date = models.DateTimeField(default=timezone.now, null=False, blank=False)
    answer_date = models.DateTimeField(null=True, blank=False)
    accept = models.BooleanField(default=False, null=False, blank=False)
    request_type_choices = [
        ('join_channel', 'join_channel'),
        ('secretary', 'secretary'),
    ]
    request_type = models.CharField(null=False, blank=False, choices=request_type_choices, default="join_channel",
                                    max_length=32)
