from decimal import Decimal
from django.db.models import Sum

from transactions.models import Expense, Income
from dashboard.services import get_month_bounds, get_summary_data

MONTH_NAMES_SHORT = [
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
]


def get_yearly_summary(user, year):
    """
    Month-by-month income/expense/surplus for the full year, reusing
    the exact same get_summary_data() function the dashboard uses —
    single source of truth for "what counts as this month's numbers."
    """
    rows = []
    total_income = Decimal('0')
    total_expense = Decimal('0')

    for month in range(1, 13):
        summary = get_summary_data(user, year, month)
        rows.append({
            'month_name': MONTH_NAMES_SHORT[month - 1],
            'income': summary['total_income'],
            'expense': summary['total_expense'],
            'surplus_deficit': summary['surplus_deficit'],
        })
        total_income += summary['total_income']
        total_expense += summary['total_expense']

    return {
        'rows': rows,
        'total_income': total_income,
        'total_expense': total_expense,
        'total_surplus': total_income - total_expense,
    }


def get_category_totals_for_year(user, year):
    """Full-year expense totals grouped by category — for the yearly breakdown chart."""
    first_day = get_month_bounds(year, 1)[0]
    last_day = get_month_bounds(year, 12)[1]

    rows = (
        Expense.objects.filter(user=user, date__gte=first_day, date__lte=last_day)
        .values('category__name')
        .annotate(total=Sum('amount'))
        .order_by('-total')
    )
    return {
        'labels': [r['category__name'] for r in rows],
        'values': [float(r['total']) for r in rows],
    }


def get_transactions_for_year(user, year):
    """
    Combined income + expense transactions for the whole year,
    used by the CSV export. Returns plain dicts (not model instances)
    so the export view doesn't need to know about two different models.
    """
    first_day = get_month_bounds(year, 1)[0]
    last_day = get_month_bounds(year, 12)[1]

    rows = []
    for income in Income.objects.filter(user=user, date__gte=first_day, date__lte=last_day):
        rows.append({
            'date': income.date,
            'type': 'Income',
            'category_or_source': income.get_source_display(),
            'description': income.description,
            'amount': income.amount,
        })
    for expense in Expense.objects.filter(user=user, date__gte=first_day, date__lte=last_day).select_related('category'):
        rows.append({
            'date': expense.date,
            'type': 'Expense',
            'category_or_source': expense.category.name,
            'description': expense.description,
            'amount': expense.amount,
        })

    rows.sort(key=lambda r: r['date'])
    return rows
