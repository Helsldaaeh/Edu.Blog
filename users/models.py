from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    first_name = None
    last_name = None
    last_login = None

    REQUIRED_FIELDS = []
    
    class Meta:
        db_table = 'users'
    def __str__(self):
        return self.username