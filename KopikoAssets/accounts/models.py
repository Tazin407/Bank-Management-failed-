from django.db import models
from django.contrib.auth.models import User
from .import constants
# Create your models here.

class UserAccount(models.Model):
    user= models.OneToOneField(User, on_delete= models.CASCADE, related_name='account')
    account_type= models.CharField(choices= constants.ACCOUNT_TYPE, max_length=30)
    account_no= models.IntegerField(unique=True)
    birth_date= models.DateField(null=True, blank=True)
    gender= models.CharField(max_length=30, choices= constants.GENDER_CHOICES)
    initial_deposit_date= models.DateField(auto_now_add=True)
    balance= models.DecimalField(default= 0, max_digits=12, decimal_places=2)
    
    def __str__(self):
        return str(self.account_no)
    
    
class UserAddress(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE, related_name='address')
    street_address= models.CharField(max_length= 30)
    postal_code=models.IntegerField()
    city= models.CharField(max_length= 30)
    country= models.CharField(max_length=30)

    def __str__(self):
        return self.user.email