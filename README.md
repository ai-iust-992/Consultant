# Consultant



Heroku admin page:
admin
admin.iust.ac.ir
admin12345


python manage.py makemigrations User calendar_ channel chat_room message 








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

    

class UserProfile(BaseUser):
    private_profile = models.BooleanField(default=False, null=False, blank=False)


class ConsultantProfile(BaseUser):
    accepted = models.BooleanField(default=False, null=False, blank=False)
    my_secretaries = models.ManyToManyField(
        UserProfile,
        related_name="my_consultants",
    )


class Lawyer(ConsultantProfile):
    certificate = models.FileField(upload_to="files/lawyers/certificate", null=True, blank=True)






==========================================================================================



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
    

class UserProfile(models.Model):
    BaseUser = models.OneToOneField(BaseUser, on_delete=models.CASCADE)
    private_profile = models.BooleanField(default=False, null=False, blank=False)


class ConsultantProfile(models.Model):
    BaseUser = models.OneToOneField(BaseUser, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False, null=False, blank=False)
    my_secretaries = models.ManyToManyField(
        UserProfile,
        related_name="my_consultants",
    )


class Lawyer(models.Model):
    consultant_profile = models.OneToOneField(ConsultantProfile, on_delete=models.CASCADE)
    certificate = models.FileField(upload_to="files/lawyers/certificate", null=True, blank=True)
