from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .import constants
from .import models

class UserRegistrationForm(UserCreationForm):
    account_type= forms.ChoiceField(choices= constants.ACCOUNT_TYPE)
    birth_date= forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    gender= forms.ChoiceField( choices= constants.GENDER_CHOICES)
    street_address= forms.CharField()
    postal_code=forms.IntegerField()
    city= forms.CharField()
    country= forms.CharField()
    
    class Meta:
        model=models.User
        fields=['username', 'first_name', 'last_name', 'email','account_type',
               'birth_date', 'gender','street_address','postal_code','city', 'country']
        
        
         
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                
                'class' : (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                ) 
            })
        
    def save(self, commit=True):
        our_user= super().save(commit=False) 
        if commit==True:
            our_user.save()#data saved into user model
            street_address= self.cleaned_data.get('street_address')
            postal_code=self.cleaned_data.get('postal_code')
            city= self.cleaned_data.get('city')
            country=self.cleaned_data.get('country')
            
            account_type= self.cleaned_data.get('account_type')
            birth_date= self.cleaned_data.get('birth_date')
            gender= self.cleaned_data.get('gender')
            
            
            models.UserAddress.objects.create(
                user= our_user,
                street_address= street_address,
                postal_code= postal_code,
                city= city,
                country= country,
            )
            
            models.UserAccount.objects.create(
                user= our_user,
                account_type= account_type,
                birth_date= birth_date,
                gender= gender,
                account_no= 1000+our_user.id,
                
            )
            
        return our_user
   
            
class UserUpdateForm(forms.ModelForm):
    account_type= forms.ChoiceField(choices= constants.ACCOUNT_TYPE)
    birth_date= forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    gender= forms.ChoiceField( choices= constants.GENDER_CHOICES)
    street_address= forms.CharField()
    postal_code=forms.IntegerField()
    city= forms.CharField()
    country= forms.CharField()
    
    class Meta:
        model=models.User
        fields=[ 'first_name', 'last_name', 'email']
        
     
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                
                'class' : (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                ) 
            })
            
        if self.instance:
            user_account= self.instance.account
            user_address= self.instance.address
            
            if user_account: #eta korle form ta existing data diye fillup thakbe
                self.fields['account_type']= user_account.account_type
                self.fields['birth_date']= user_account.birth_date
                self.fields['gender']= user_account.gender
                self.fields['street_address']= user_address.street_address
                self.fields['postal_code']= user_address.postal_code
                self.fields['city']= user_address.city
                self.fields['country']= user_address.country
    
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()

            user_account, created = models.UserAccount.objects.get_or_create(user=user) # jodi account thake taile seta jabe user_account ar jodi account na thake taile create hobe ar seta created er moddhe jabe
            user_address, created = models.UserAddress.objects.get_or_create(user=user) 

            user_account.account_type = self.cleaned_data['account_type']
            user_account.gender = self.cleaned_data['gender']
            user_account.birth_date = self.cleaned_data['birth_date']
            user_account.save()

            user_address.street_address = self.cleaned_data['street_address']
            user_address.city = self.cleaned_data['city']
            user_address.postal_code = self.cleaned_data['postal_code']
            user_address.country = self.cleaned_data['country']
            user_address.save()

        return user
    
    
    