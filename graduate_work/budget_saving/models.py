from django.db import models

class Expenses_for_period(models.Model):
    many = models.DecimalField(max_digits=10, decimal_places=2, default=0)

class Expenses_per_day(models.Model):
    many = models.DecimalField(max_digits=10, decimal_places=2, default=0)

class Balance_of_expenses(models.Model):
    many = models.DecimalField(max_digits=10, decimal_places=2, default=0)

class DatePeriod(models.Model):
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    total_money = models.FloatField(default=0.0)


class Expense_table(models.Model):
    remaining_days = models.IntegerField(default=0)
    dates = models.ForeignKey(DatePeriod, on_delete=models.CASCADE)
    expenses = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    remainder = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    alt_remainder = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    saving = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    expenses_for_period = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    expenses_per_day = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    savings = models.ForeignKey(Balance_of_expenses, on_delete=models.DO_NOTHING, default=1)

