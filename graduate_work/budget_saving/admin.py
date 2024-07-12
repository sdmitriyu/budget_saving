from django.contrib import admin
from .models import Expenses_for_period, Expenses_per_day, Balance_of_expenses, Expense_table


admin.site.register(Expenses_for_period)
admin.site.register(Expenses_per_day)
admin.site.register(Balance_of_expenses)
admin.site.register(Expense_table)

