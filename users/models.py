from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_buyer = models.BooleanField(default=False)
    is_supplier = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_china = models.BooleanField(default=True)
    is_thai_inbound = models.BooleanField(default=True)
    is_thai_outbound = models.BooleanField(default=True)
