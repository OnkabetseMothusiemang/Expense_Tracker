from django import forms
from .models import Expense
from .models import UserProfile

class SalaryForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['salary']

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'amount', 'description']
