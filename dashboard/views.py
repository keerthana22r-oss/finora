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
def home_view(request):
    today = date.today()

    try:
        year = int(request.GET.get('year', today.year))
        month = int(request.GET.get('month', today.month))
        if month < 1 or month > 12:
            month = today.month
    except (ValueError, TypeError):
        year, month = today.year, today.month

    summary = services.get_summary_data(request.user, year, month)
    bar_chart = services.get_income_vs_expense_chart_data(request.user, year, month)
    doughnut_chart = services.get_category_breakdown_chart_data(request.user, year, month)
    trend_chart = services.get_monthly_trend_chart_data(request.user, year, month)
    budget_overview = services.get_budget_overview(request.user, year, month)
    savings_overview = services.get_savings_overview(request.user)

    year_options = list(range(today.year - 3, today.year + 1))

    return render(request, 'dashboard/home.html', {
        'summary': summary,
        'bar_chart': bar_chart,
        'doughnut_chart': doughnut_chart,
        'trend_chart': trend_chart,
        'budget_overview': budget_overview,
        'savings_overview': savings_overview,
        'selected_month': month,
        'selected_year': year,
        'month_names': MONTH_NAMES,
        'year_options': year_options,
        'selected_month_label': dict(MONTH_NAMES).get(month, ''),
    })
