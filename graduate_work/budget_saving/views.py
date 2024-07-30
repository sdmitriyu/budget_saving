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
        many = request.POST.get('many')
        my_expenses = request.POST.get('my_expenses')

        # Проверка на все необходимые поля
        # if not start_date or not end_date or not many or not my_expenses:

            # return render(request, 'date_period_form.html', {'error': 'Не все поля заполнены!'})

        # Обработка и преобразование дат
        start_date = timezone.datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d').date()

        # Расчёты и добавление в базу данных
        Expenses_per_day.object.ceate(many=many)  # Сохраняем расходы на день

        days = (end_date - start_date).days  # Количество дней
        days = float(days)

        expenses_for_period_calculation = days * float(many)  # Планируемая сумма расходов за период
        expenses_for_period = Expenses_for_period(many=expenses_for_period_calculation)
        expenses_for_period.save()  # Сохраняем расходы на период в базу данных
        dates = [start_date, end_date]
        # res = pd.date_range(start_date, end_date).strftime('%d/%m/%Y').tolist()  # Расчёт диапазона дней периода
        date_period = DatePeriod(start_date=min(dates), end_date=max(dates))
        Expense_table.objects.create(dates=date_period)  # Сохраняем диапазон дат периода

        rest_of_days_calculation = range(days, 0, -1)  # Получение оставшихся дней
        for day in rest_of_days_calculation:
            Expense_table.objects.create(remaining_days=day)

        for date in date_period:
            date_period_entry = Expense_table.objects.get(date=date)

            Expense_table.objects.update_or_create(
                date=date_period_entry,
                defaults={
                    'expenses': my_expenses,
                })

        # Получение последнего объекта с балансом
        all_expenses = Expense_table.objects.aggregate(total=Sum('expenses'))
        sum_expenses = all_expenses['total']
        balance_of_expenses = sum_expenses-expenses_for_period
        Balance_of_expenses.object.save(many=balance_of_expenses)

        remainder = 0
        for date in Expense_table.dates:
            # Получение записи DatePeriod по дате
            date_period_entry = Expense_table.objects.get(dates=date)
            # Прибавление ежедневных расходов к остатку
            remainder += Expenses_per_day.objects.get(many=many)
            # Получение уже существующих расходов для данной даты (если есть)
            existing_expense = Expense_table.objects.filter(date=date).first()
            if existing_expense:
                # Вычитаем уже существующие расходы из остатка
                remainder -= existing_expense.expenses
            # Обновление или создание записи в Expense_table
            Expense_table.objects.update_or_create(
                date=date_period_entry,
                defaults={
                    'my_expenses': expenses,
                }
            )

        try:
            table = Expense_table.object.get(dates=dates)
            return Expense_table.remaining_days
        except Expense_table.DoesNotExist:
            return None
        remaining_days = Expense_table.remaining_days
        alt_remainder = balance_of_expenses / remaining_days
        Expense_table.object.ceate(alt_remainder=alt_remainder)




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