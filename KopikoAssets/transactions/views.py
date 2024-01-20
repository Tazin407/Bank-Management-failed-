from typing import Any
from django.shortcuts import render, redirect, get_list_or_404
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, View
from django.urls import reverse_lazy
from .import models
from .import forms
from django.db.models import Sum
from django.contrib import messages
from django.http import HttpResponse
from transactions.constants import DEPOSIT, WITHDRAWAL,LOAN, LOAN_PAID

class TransactionCreateMixin(LoginRequiredMixin, CreateView):
    model= models.Transaction
    title= ''
    template_name= 'transaction_form.html'
    success_url='deposit_money'
    
    # def get_form_kwargs(self) -> dict[str, Any]:
    #     return super().get_form_kwargs()
    
    #eta form er init e account ke pass korbe
    def get_form_kwargs(self):
        kwargs= super().get_form_kwargs()
        kwargs.update({
            'account': self.request.user.account
        })
        return kwargs
    
    # def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    #     return super().get_context_data(**kwargs)
    
    #ei function ta nilam just title ta pass korar jonno 
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context.update({
            'title': self.title
        })

        return context
    
class DepositView(TransactionCreateMixin):
    form_class=forms.DepositForm
    title='Diposit Money'
    print('Deposit')
    
    def get_initial(self):
        initial= {'transaction_type': DEPOSIT}
        return initial

    # get_initial kete diye ei success_url ta use korle kaj hoy
    def get_success_url(self):
        print(self.request.path)
        return self.request.path
    
    def form_valid(self, form):
        
        amount=form.cleaned_data.get('amount')
        account= self.request.user.account
        account.balance += amount
        
        account.save(
            update_fields=['balance']
        )
        
        messages.success(self.request, f"{amount} BDT has been successfully deposited")
        
        return super().form_valid(form)
    
class WithdrawView(TransactionCreateMixin):
    form_class= forms.WithdrawForm
    title= 'Withdraw Money'
    print('amount')
    
    def get_initial(self):
        initial= {'transaction_type': WITHDRAWAL}
        return initial
    
    def form_valid(self, form):
        amount= form.cleaned_data['amount']
        account= self.request.user.account
        account.balance-=amount
        
        account.save(
            update_fields=['balance']
        )
        messages.success(self.request, f"{amount} BDT has been successfully withdrawed")
        return super().form_valid(form)
    
    
class LoanRequView(TransactionCreateMixin):
    form_class= forms.LoanRequForm
    title= 'Loan Request'
    
    def get_initial(self):
        initial= {'transaction_type': LOAN}
        return initial
    
    def form_valid(self, form):
        amount= form.cleaned_data.get('amount')
        current_loan_count= models.Transaction.objects.filter(account= self.request.user.account,
            loan_approve=True,transaction_type= 'Loan').count()
        
        if current_loan_count >=3:
            return HttpResponse(f"You have reached your loan limit")
        
        messages.success(self.request, f"{amount} BDT has been requested for loan. Please wait for the approval")
        
        
        return super().form_valid(form)
    
class TransactionReportView(LoginRequiredMixin, ListView):
    model= models.Transaction
    template_name ='transaction_report.html'
    
    def get_queryset(self):
        queryset= super().get_queryset().filter(
            account= self.request.user.account
        )
        
        start_date_str= self.request.GET.get('start_date')
        end_date_str= self.request.GET.get('end_date')
        
        if start_date_str and end_date_str:
            start_date= datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date= datetime.strptime(end_date_str, "%Y-%m-%d").date()
            
            queryset= queryset.filter(timestamp_date__gte= start_date, timestamp_date__lte=end_date)
            self.balance= models.Transaction.objects.filter().aggregate(Sum('amount'))['amount__sum']
            
        else:
            self.balance= self.request.user.account.balance
            
        return queryset.distinct()
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context= super().get_context_data(**kwargs)
        context.update({
            'account': self.request.user.account
        })
        return context
        
        
class PayLoanView(LoginRequiredMixin, View):
    def get(self, request, loan_id):
        loan = get_list_or_404(models.Transaction, id= loan_id)
        
        if loan.loan_approve:
            user_account= loan.account
            if loan.amount < user_account.balance:
                user_account.balance -= loan.amount
                loan.balance_after_transaction= user_account.balance
                user_account.save()
                loan.transaction_type= TRANSACTION_CHOICES['loan_paid']
                loan.save()
                
                return redirect('transaction_report')
            else:
                messages.error(self.request, f'Not enough balance')
                
        return redirect('transaction_report')
    
class LoanListView(LoginRequiredMixin, ListView):
    model= models.Transaction
    context_object_name= 'loans'
    
    def get_queryset(self):
        user_account= self.request.user.account
        queryset= models.Transaction.objects.filter(account= user_account, transaction_type= TRANSACTION_CHOICES['loan'])
        return queryset
        
    
    
    
