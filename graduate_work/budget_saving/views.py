from django.shortcuts import render
from .forms import DatePeriodForm
from .models import DatePeriod


def date_period_view(request):
    if request.method == 'POST':
        form = DatePeriodForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            total_money = form.cleaned_data['total_money']

            period = (end_date - start_date).days
            money_per_day = total_money / period

            # Сохраняем данные в базу данных
            DatePeriod.objects.create(
                start_date=start_date,
                end_date=end_date,
                total_money=total_money
            )

            for i in range(period, 0, -1):
                DatePeriod.objects.create(
                    start_date=start_date,
                    end_date=end_date,
                    total_money=money_per_day
                )

            return render(request, 'date_period_result.html')
    else:
        form = DatePeriodForm()

    return render(request, 'date_period_form.html', {'form': form})


def budget_saving():
    return None