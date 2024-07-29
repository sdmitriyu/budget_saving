from django import forms
from .models import DatePeriod, Expenses_per_day, Expense_table

class DatePeriodForm(forms.ModelForm):
    class Meta:
        model = DatePeriod
        fields = ['start_date', 'end_date',]

class ExpensesPerDayForm(forms.ModelForm):
    class Meta:
        model = Expenses_per_day
        fields = ['many']

class ExpensesForm(forms.ModelForm):
    class Meta:
        model = Expense_table
        fields = ['my_expenses']