from django.shortcuts import render
from datetime import datetime, timedelta

# Create your views here.
def calculate_working_days(request):
    if request.method == 'POST':
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        holidays_str = request.POST.get('holidays')

        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        holidays = holidays_str.split(',')

        working_days = 0
        current_date = start_date
        while current_date <= end_date:
            if current_date.weekday() < 5 and current_date.strftime('%Y-%m-%d') not in holidays:
                working_days += 1
            current_date += timedelta(days=1)

        return render(request, 'cash_collection/result.html', {'working_days': working_days})

    return render(request, 'cash_collection/calculate.html')
