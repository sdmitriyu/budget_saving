from django import forms
from .models import DatePeriod, Expenses_per_day

class DatePeriodForm(forms.ModelForm):
    class Meta:
        model = DatePeriod
        fields = ['start_date', 'end_date', 'total_money']

class ExpensesPerDayForm(forms.ModelForm):
    class Meta:
        model = Expenses_per_day
        fields = ['many']
