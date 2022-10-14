from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Model
from django.utils import timezone
from datetime import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError


# Create your models here.
class Streets(models.Model):
    street = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.street.title()} "


class Helps(models.Model):
    help = models.DateTimeField(default=(datetime.now))
    Check = models.BooleanField()


# def save(self, *args, **kwargs):
#     if self.Check and self.help is None:
#         self.help = timezone.now()
#     elif not self.Check and self.help is not None:
#         self.help = None
#     super(Model, self).save(*args, **kwargs)

class User(AbstractUser):
    # userLot = models.ForeignKey(Lot, on_delete=models.CASCADE, related_name="userLot")
    home = models.PositiveIntegerField(null=True, )
    patronymic = models.CharField(max_length=24)
    apartment = models.PositiveIntegerField(blank=True, null=True, )
    # date_birth = models.DateTimeField()
    phone = models.CharField(max_length=10)
    invalid = models.CharField(max_length=20, unique=True, null=True, blank=True, default=None)
    pension = models.CharField(max_length=30, unique=True, null=True, blank=True, default=None)
    many_children = models.CharField(max_length=20, unique=True, null=True, blank=True, default=None)
    street = models.ForeignKey(Streets, on_delete=models.CASCADE, related_name="user_street", null=True, )
    helps = models.ManyToManyField(Helps, blank=True, related_name="helpmy")
    date_birth = models.DateField(null=True, blank=True)
    home_index = models.CharField(max_length=1, blank=True, null=True,
                                  choices=[('а', "а"), ('б', "б"), ('в', "в"), ('г', "г")])
    apartment_index = models.CharField(max_length=1, blank=True, null=True,
                                       choices=[('а', "а"), ('б', "б"), ('в', "в"), ('г', "г")])

    class Meta:
        unique_together = ('street', 'home', 'home_index', 'apartment', 'apartment_index',)
    def __str__(self):
        return f"{self.last_name.title()} "
    # def clean(self):
    #     if self.invalid == '':
    #         self.invalid = None

    # def save(self, commit=True):
    #     if self.instance.pension == '':
    #         self.instance.pension = None
    #     return super().save(commit)

    # def clean(self):
    #     if self.apartment is None:
    #         self.apartment = 0        # def clean(self, *args, **kwargs):
    #     # run the base validation
    #     super(User, self).clean(*args, **kwargs)
    #
    #     # Don't allow dates older than now.
    #     if self.date_birth < datetime.datetime.now():
    #         raise ValidationError('Start time must be later than now.')
