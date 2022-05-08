from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    GENDER_CHOICES = (('male', 'male'), ('female', 'female'))

    genres = models.CharField(max_length=50)
    gender = models.CharField(default='male',max_length=10, choices=GENDER_CHOICES)
    year = models.IntegerField(default=2000)
    month = models.IntegerField(default=1)
    day = models.IntegerField(default=1)