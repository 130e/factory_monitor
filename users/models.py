from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

# Create your models here.
class User(AbstractUser):
    email_code = models.CharField(max_length=20, default="default")
    is_active = models.BooleanField(default=True)
    
    class Meta(AbstractUser.Meta):
        pass