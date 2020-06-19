from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


class Country(models.Model):
    name = models.CharField(max_length=32, unique=True)


class City(models.Model):
    name = models.CharField(max_length=32, db_index=True)


class Address(models.Model):
    address1 = models.CharField(max_length=128)
    address2 = models.CharField(max_length=128, blank=True)
    zip_code = models.PositiveSmallIntegerField()

    city = models.ForeignKey(to='City', on_delete=models.CASCADE)


class Dealer(AbstractUser):
    address = models.ForeignKey(to='Address', on_delete=models.CASCADE)
