from django.db import models


class Expenses_for_period(models.Model):
    many = models.DecimalField(max_digits=10, decimal_places=2)


class Expenses_per_day(models.Model):
    many = models.DecimalField(max_digits=10, decimal_places=2)


class Balance_of_expenses(models.Model):
    many = models.DecimalField(max_digits=10, decimal_places=2)

class DatePeriod(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    total_money = models.FloatField()


class Expense_table(models.Model):
    remaining_days = models.IntegerField()
    date = models.ForeignKey(DatePeriod, on_delete=models.CASCADE)
    expenses = models.DecimalField(max_digits=10, decimal_places=2)
    remainder = models.DecimalField(max_digits=10, decimal_places=2)
    alt_remainder = models.DecimalField(max_digits=10, decimal_places=2)
    saving = models.DecimalField(max_digits=10, decimal_places=2)
    expenses_for_period = models.ForeignKey(Expenses_for_period, on_delete=models.DO_NOTHING)
    expenses_per_day = models.ForeignKey(Expenses_per_day, on_delete=models.DO_NOTHING)
    balance_of_expenses = models.ForeignKey(Balance_of_expenses, on_delete=models.DO_NOTHING)

