from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
 

class User(AbstractUser):
    email = models.EmailField(unique=True, null = False )
    username = models.CharField(max_length=100)
    bio = models.CharField(max_length=100)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS =['username']

    def __str__(self):
        return self.username
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="image", null=True, blank=True)
    full_name = models.CharField(max_length=200, null=True, blank=True)
    bio = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200)
    address = models.CharField(max_length=200, null=True, blank=True)
    county = models.CharField(max_length=200, null=True, blank=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name if self.full_name else self.user.username
