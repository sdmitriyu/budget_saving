import pandas as pd
from django.shortcuts import render
from django.utils import timezone
from .models import Expenses_per_day, Expense_table, Balance_of_expenses, Expenses_for_period


def date_period_form(request):
    return render(request, 'date_period_form.html')

def expenses(request):
    return render(request, 'expenses.html')


# noinspection PyTypeChecker
def calculate_expenses(request):
    if request.method == 'POST':
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        many = request.POST['many']
        expenses = request.POST['expenses']

        # Обработка и преобразование дат
        start_date = timezone.datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d').date()

        # Расчёты и добавление в базу данных
        expenses_per_day = Expenses_per_day(many=many)
        expenses_per_day.save()  # Сохраняем расходы на день

        days = (end_date - start_date).days  # Количество дней

        expenses_for_period_calculation = days * many  # Планируемая сумма расходов за период
        expenses_for_period = Expenses_for_period(many=expenses_for_period_calculation)
        expenses_for_period.save()  # Сохраняем расходы на период в базу данных

        # Получение последнего объекта с балансом
        last_expense = float(expenses_for_period) - float(expenses)
        last_expense = Balance_of_expenses.many.filter(date__range=[start_date, end_date]).last()
        balance_of_expenses_calculation = last_expense.remainder if last_expense else 0
        balance_of_expenses = Balance_of_expenses(many=balance_of_expenses_calculation)
        balance_of_expenses.save()

        # start_date = datetime.date(start_date)
        # end_date = datetime.date(end_date)

        res = pd.date_range(
            min(start_date, end_date),
            max(start_date, end_date)
        ).strftime('%d/%m/%Y').tolist()  # Расчёт диапазона дней периода
        date_entry = Expense_table(date=res)
        date_entry.save()  # Сохраняем диапазон дат периода

        rest_of_days_calculation = range(1, int(days), -1)
        remaining_days = Expense_table(remaining_days=rest_of_days_calculation)
        remaining_days.save()


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

