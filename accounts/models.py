from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    USERNAME_FIELD = 'email'        # Email becomes login
    REQUIRED_FIELDS = ['username']  # username is still required by AbstractUser

    def __str__(self):
        return self.email
    

class Profile(models.Model):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE)
    address = models.TextField(blank=True)
    default_shipping = models.BooleanField(default=False)
    saved_cart = models.JSONField(blank=True, null=True)  # optional for later cart storage

    def __str__(self):
        return f"{self.user.email} Profile"