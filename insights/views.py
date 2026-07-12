from datetime import date
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from . import services


MONTH_NAMES = [
    (1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'),
    (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'),
    (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December'),
]


@login_required
def insights_view(request):
    today = date.today()

    try:
        year = int(request.GET.get('year', today.year))
        month = int(request.GET.get('month', today.month))
        if month < 1 or month > 12:
            month = today.month
    except (ValueError, TypeError):
        year, month = today.year, today.month

    insights_list = services.generate_insights(request.user, year, month)
    year_options = list(range(today.year - 3, today.year + 1))

    return render(request, 'insights/insights_list.html', {
        'insights_list': insights_list,
        'selected_month': month,
        'selected_year': year,
        'month_names': MONTH_NAMES,
        'year_options': year_options,
    })
