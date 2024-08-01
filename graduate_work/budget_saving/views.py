import pandas as pd
from django.db.models import Sum
from django.shortcuts import render
from django.utils import timezone
from .models import Expenses_per_day, Expense_table, Balance_of_expenses, Expenses_for_period, DatePeriod

def date_period_form(request):
    return render(request, 'date_period_form.html')

def expenses(request):
    return render(request, 'expenses.html')


def calculate_expenses(request):
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        many = float(request.POST.get('many'))  # Преобразуем сразу в float
        my_expenses = float(request.POST.get('my_expenses'))

        if not start_date or not end_date or not many or not my_expenses:
            return render(request, 'date_period_form.html', {'error': 'Не все поля заполнены!'})

        start_date = timezone.datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d').date()

        DatePeriod.objects.create(start_date=start_date, end_date=end_date)
        Expenses_per_day.objects.create(many=many)

        days = (end_date - start_date).days
        expenses_for_period_calculation = days * many
        expenses_for_period = Expenses_for_period(many=expenses_for_period_calculation)
        expenses_for_period.save()

        # Обработка диапазона дат
        for single_date in pd.date_range(start_date, end_date):
            Expense_table.objects.update_or_create(
                date=single_date,
                defaults={'expenses': my_expenses}
            )

        all_expenses = Expense_table.objects.aggregate(total=Sum('expenses'))
        sum_expenses = all_expenses['total'] if all_expenses['total'] else 0
        balance_of_expenses = sum_expenses - expenses_for_period_calculation

        Balance_of_expenses.objects.create(many=balance_of_expenses)

        # Логика остатка
        remainder = 0
        for single_date in pd.date_range(start_date, end_date):
            existing_expense = Expense_table.objects.filter(date=single_date).first()
            if existing_expense:
                remainder -= existing_expense.expenses
            remainder += many  # Каждый день добавляем расходы
            Expense_table.objects.update_or_create(
                date=single_date,
                defaults={'my_expenses': my_expenses}
            )

            remaining_days = days
            alt_remainder = balance_of_expenses / remaining_days if remaining_days > 0 else 0
            Expense_table.objects.create(alt_remainder=alt_remainder)

            savings = many - my_expenses
            Expense_table.objects.create(savings=savings)

            return render(request, 'date_period_result.html')

            return render(request, 'date_period_form.html')



def result(request):


    context = {
        'expenses_for_period': Expenses_for_period.many,
        'expenses_per_day': Expenses_per_day.many,
        'balance_of_expenses': Balance_of_expenses.many,
        'remaining_days': Expense_table.remaining_days,
        'dates': Expense_table.date,
        'expenses': Expense_table.expenses,
        'remainder': Expense_table.remainder,
        'alt_remainder': Expense_table.alt_remainder,
        'saving': Expense_table.saving
        }

    return render(request, 'date_period_result.html', context)