from django import forms 
from .import models

class TransactionForm(forms.ModelForm):
    class Meta:
        model= models.Transaction
        fields=['amount', 'transaction_type']
        
    #transaction_type user dekbe na. eta hide korar jnno constructor e kaj korlam
    def __init__(self, *args, **kwargs):
        self.account= kwargs.pop('account')#kwargs theke account ke pop kore anlam 
        #eta korle barbar user ke logged in proman korte hobe na
        
        #pop er bodole get dileo hoito
        
        super().__init__(*args, **kwargs)
        self.fields['transaction_type'].disabled = True
        self.fields['transaction_type'].widget= forms.HiddenInput()
        
    def save(self, commit=True):
        self.instance.account= self.account
        self.instance.balance_after_trans= self.balance
        return super().save()
    

class DepositForm(TransactionForm):
    def cleaned_amount(self): #amount ke filter korbo
        minimum_amount=100
        amount= self.cleaned_data.get('amount')
        if amount < minimum_amount:
            raise forms.ValidationError(
                f'You can not diposit less than {minimum_amount} BDT'
            )
            
        return amount
    
class WithdrawForm(TransactionForm):
    
    def cleaned_amount(self):
        account= self.account #account ta ansi balance ber korar jnno
        amount= self.cleaned_data.get('amount')
        balance= account.balance
        
        if amount > balance:
            raise forms.ValidationError(
                f'You have only {balance} BDT left in your account.you can not withdraw more than your balance.'
            )
            
        return amount
    
class LoanRequForm(TransactionForm):
    
    def cleaned_amount(self):
        amount= self.cleaned_data.get('amount')
        
        return amount
    