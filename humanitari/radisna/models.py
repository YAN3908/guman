from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError


# Create your models here.
# class Street(models.Model):
#     category = models.CharField(max_length=64)


class User(AbstractUser):
    # userLot = models.ForeignKey(Lot, on_delete=models.CASCADE, related_name="userLot")
    home = models.IntegerField()
    patronymic = models.CharField(max_length=24)
    apartment = models.IntegerField()
    date_birth = models.DateTimeField()
    phone = models.CharField(max_length=10)
    invalid = models.CharField(max_length=20, blank=True)
    many_children = models.CharField(max_length=20, blank=True)
    # street = models.ForeignKey(Street, on_delete=models.CASCADE, related_name="user_street")
    # date_birth = models.DateField(null=True, blank=True)
    # def clean(self, *args, **kwargs):
    #     # run the base validation
    #     super(User, self).clean(*args, **kwargs)
    #
    #     # Don't allow dates older than now.
    #     if self.date_birth < datetime.datetime.now():
    #         raise ValidationError('Start time must be later than now.')



