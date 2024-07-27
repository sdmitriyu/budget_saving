from django.shortcuts import render, redirect
from .forms import DatePeriodForm, ExpensesPerDayForm
from .models import DatePeriod, Expenses_per_day, Expense_table, Balance_of_expenses, Expenses_for_period
from django.utils import timezone
from datetime import timedelta  # Не забывайте импортировать timedelta


def date_period_form(request):
    return render(request, 'date_period_form.html')

def expenses(request):
    return render(request, 'expenses.html')


def calculate_expenses(request):
    if request.method == 'POST':
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        many = request.POST['many']

        # Обработка и преобразование дат
        start_date = timezone.datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d').date()

        days = (end_date - start_date).days  # Количество дней
        Expenses_per_day.many = many
        expenses_for_period = days * many  # Планируемая сумма расходов за период
        Expenses_for_period.many = expenses_for_period  # Сохраняем расходы на период в базу данных
        deltaday = range(start_date, end_date)


        # Для вывода в шаблон

        # Далее выщитываем
        expenses_per_day = Expenses_per_day

        # Получение последнего объекта с балансом
        last_expense = Expense_table.objects.filter(date__range=[start_date, end_date]).last()
        balance_of_expenses = last_expense.remainder if last_expense else 0

        # Получение списка записей таблицы расходов
        expense_table_entries = Expense_table.objects.filter(date__range=[start_date, end_date])

        # Передаем данные в шаблон
        context = {
            'expenses_for_period': expenses_for_period,
            'expenses_per_day': expenses_per_day,
            'balance_of_expenses': balance_of_expenses,
            'expense_table_entries': expense_table_entries,
        }
        return render(request, 'date_period_result.html', context)

    return render(request, 'date_period_form.html')


def input_data(request):
    if request.method == 'POST':
        date_form = DatePeriodForm(request.POST)
        expenses_form = ExpensesPerDayForm(request.POST)

        if date_form.is_valid() and expenses_form.is_valid():
            date_period = date_form.save()
            expenses_per_day = expenses_form.save()

            # Расчет и сохранение данных
            total_days = (date_period.end_date - date_period.start_date).days + 1
            expenses_for_period = Expenses_for_period.objects.create(many=expenses_per_day.many * total_days)

            # Заполнение таблицы расходов
            for day in range(total_days):
                date_entry = date_period.start_date + timedelta(days=day)
                remainder = expenses_for_period.many - expenses_per_day.many * (day + 1)
                alt_remainder = remainder / (total_days - (day + 1)) if (total_days - (day + 1)) > 0 else 0

                Expense_table.objects.create(
                    remaining_days=total_days - day,
                    date=date_entry,
                    expenses=expenses_per_day.many,
                    remainder=remainder,
                    alt_remainder=alt_remainder,
                    saving=0
                )

            return redirect('result')
    else:
        date_form = DatePeriodForm()
        expenses_form = ExpensesPerDayForm()

    return render(request, 'date_period_form.html', {'date_form': date_form, 'expenses_form': expenses_form})


def result(request):
    # expenses_for_period = Expenses_for_period.objects.last()
    # expenses_per_day = Expenses_per_day.objects.last()

    expense_table_entries = Expense_table.objects.filter(
        expenses_for_period=expenses_for_period
    ).order_by('date')

    last_entry = expense_table_entries.last()

    balance_of_expenses = last_entry.balance_of_expenses if last_entry else None

    context = {
        'expenses_for_period': expenses_for_period,
        'expenses_per_day': expenses_per_day,
        'balance_of_expenses': balance_of_expenses,
        'expense_table_entries': expense_table_entries,
    }

    return render(request, 'date_period_result.html', context)
