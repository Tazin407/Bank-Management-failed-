from django.db import models
from accounts.models import UserAccount
from .import constants

# Create your models here.
class Transaction(models.Model):
    account= models.ForeignKey(UserAccount, on_delete= models.CASCADE)
    amount= models.DecimalField(decimal_places=2, max_digits=12)
    transaction_type= models.CharField(max_length=20, choices=constants.TRANSACTION_CHOICES, blank=True)
    balance_after_trans= models.DecimalField(decimal_places=2, max_digits=12)
    
    timestamp= models.DateTimeField(auto_now_add=True)
    loan_approve = models.BooleanField(default=False) 
    
    class Meta:
        ordering= ['timestamp']