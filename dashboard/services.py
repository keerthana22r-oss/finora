import calendar
from datetime import date
from decimal import Decimal
from dateutil.relativedelta import relativedelta

from django.db.models import Sum
from django.db.models.functions import TruncMonth

from transactions.models import Income, Expense


def get_month_bounds(year, month):
    """Returns (first_day, last_day) date objects for the given month/year."""
    first_day = date(year, month, 1)
    last_day_num = calendar.monthrange(year, month)[1]
    last_day = date(year, month, last_day_num)
    return first_day, last_day


def get_summary_data(user, year, month):
    """
    Core dashboard numbers for one month:
    total income, total expenses, surplus/deficit, and top spending category.
    Uses Sum() aggregation so the database does the math, not Python loops.
    """
    first_day, last_day = get_month_bounds(year, month)

    income_qs = Income.objects.filter(user=user, date__gte=first_day, date__lte=last_day)
    expense_qs = Expense.objects.filter(user=user, date__gte=first_day, date__lte=last_day)

    total_income = income_qs.aggregate(total=Sum('amount'))['total'] or Decimal('0')
    total_expense = expense_qs.aggregate(total=Sum('amount'))['total'] or Decimal('0')
    surplus_deficit = total_income - total_expense

    top_category_row = (
        expense_qs.values('category__name', 'category__icon')
        .annotate(total=Sum('amount'))
        .order_by('-total')
        .first()
    )

    return {
        'total_income': total_income,
        'total_expense': total_expense,
        'surplus_deficit': surplus_deficit,
        'is_surplus': surplus_deficit >= 0,
        'top_category_name': top_category_row['category__name'] if top_category_row else None,
        'top_category_icon': top_category_row['category__icon'] if top_category_row else None,
        'top_category_amount': top_category_row['total'] if top_category_row else Decimal('0'),
    }


def get_income_vs_expense_chart_data(user, year, month, months_back=6):
    """
    Returns labels + income/expense totals for the last `months_back` months
    (including the selected month), for the grouped bar chart.
    """
    selected = date(year, month, 1)
    labels = []
    income_totals = []
    expense_totals = []

    # Walk backwards from the selected month so the chart always ends
    # on whatever month the user has filtered to, not necessarily "today".
    for i in range(months_back - 1, -1, -1):
        target_date = selected - relativedelta(months=i)
        first_day, last_day = get_month_bounds(target_date.year, target_date.month)

        month_income = Income.objects.filter(
            user=user, date__gte=first_day, date__lte=last_day
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0')

        month_expense = Expense.objects.filter(
            user=user, date__gte=first_day, date__lte=last_day
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0')

        labels.append(target_date.strftime('%b %Y'))
        income_totals.append(float(month_income))
        expense_totals.append(float(month_expense))

    return {'labels': labels, 'income': income_totals, 'expense': expense_totals}


def get_category_breakdown_chart_data(user, year, month):
    """Expense totals grouped by category, for the doughnut chart. Only non-zero categories shown."""
    first_day, last_day = get_month_bounds(year, month)

    rows = (
        Expense.objects.filter(user=user, date__gte=first_day, date__lte=last_day)
        .values('category__name')
        .annotate(total=Sum('amount'))
        .order_by('-total')
    )

    labels = [row['category__name'] for row in rows]
    values = [float(row['total']) for row in rows]
    return {'labels': labels, 'values': values}


def get_monthly_trend_chart_data(user, year, month, months_back=6):
    """Expense totals per month for the trend line chart — same window as the bar chart."""
    selected = date(year, month, 1)
    labels = []
    totals = []

    for i in range(months_back - 1, -1, -1):
        target_date = selected - relativedelta(months=i)
        first_day, last_day = get_month_bounds(target_date.year, target_date.month)

        month_total = Expense.objects.filter(
            user=user, date__gte=first_day, date__lte=last_day
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0')

        labels.append(target_date.strftime('%b %Y'))
        totals.append(float(month_total))

    return {'labels': labels, 'values': totals}
