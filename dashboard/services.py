import calendar
from datetime import date
from decimal import Decimal
from dateutil.relativedelta import relativedelta

from django.db.models import Sum

from transactions.models import Income, Expense


def get_month_bounds(year, month):
    first_day = date(year, month, 1)
    last_day_num = calendar.monthrange(year, month)[1]
    last_day = date(year, month, last_day_num)
    return first_day, last_day


def get_summary_data(user, year, month):
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
    selected = date(year, month, 1)
    labels, income_totals, expense_totals = [], [], []

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
    selected = date(year, month, 1)
    labels, totals = [], []

    for i in range(months_back - 1, -1, -1):
        target_date = selected - relativedelta(months=i)
        first_day, last_day = get_month_bounds(target_date.year, target_date.month)

        month_total = Expense.objects.filter(
            user=user, date__gte=first_day, date__lte=last_day
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0')

        labels.append(target_date.strftime('%b %Y'))
        totals.append(float(month_total))

    return {'labels': labels, 'values': totals}


def get_budget_overview(user, year, month):
    """Aggregates ALL budgets for the month into one overall percentage."""
    from transactions.models import Budget

    budgets = Budget.objects.filter(user=user, year=year, month=month)

    if not budgets.exists():
        return {'has_budgets': False}

    total_limit = budgets.aggregate(total=Sum('limit_amount'))['total'] or Decimal('0')

    first_day, last_day = get_month_bounds(year, month)
    budgeted_category_ids = budgets.values_list('category_id', flat=True)
    total_spent = Expense.objects.filter(
        user=user, category_id__in=budgeted_category_ids,
        date__gte=first_day, date__lte=last_day
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0')

    percentage = (total_spent / total_limit * 100) if total_limit > 0 else Decimal('0')

    if percentage >= 100:
        color = 'danger'
    elif percentage >= 80:
        color = 'warning'
    else:
        color = 'success'

    return {
        'has_budgets': True,
        'total_limit': total_limit,
        'total_spent': total_spent,
        'percentage': min(percentage, Decimal('100')),
        'raw_percentage': percentage,
        'color': color,
    }


def get_savings_overview(user):
    """
    Aggregates ALL savings goals into one overall progress number for the
    dashboard card. Import is deferred to avoid a circular import with
    goals/services.py.
    """
    from goals.models import SavingsGoal

    goals = SavingsGoal.objects.filter(user=user)

    if not goals.exists():
        return {'has_goals': False}

    total_target = goals.aggregate(total=Sum('target_amount'))['total'] or Decimal('0')
    total_saved = goals.aggregate(total=Sum('current_amount'))['total'] or Decimal('0')

    percentage = (total_saved / total_target * 100) if total_target > 0 else Decimal('0')

    return {
        'has_goals': True,
        'goal_count': goals.count(),
        'total_target': total_target,
        'total_saved': total_saved,
        'percentage': min(percentage, Decimal('100')),
        'raw_percentage': percentage,
    }


def get_subscriptions_overview(user):
    """
    Lightweight dashboard-card version of the subscription overview —
    just the totals, not the full per-subscription breakdown (that lives
    on the dedicated Subscriptions page). Import deferred to avoid
    circular imports between dashboard and subscriptions services.
    """
    from subscriptions.services import get_subscription_overview as full_overview

    result = full_overview(user)
    return {
        'has_subscriptions': result['active_count'] > 0,
        'total_monthly': result['total_monthly'],
        'active_count': result['active_count'],
        'upcoming_count': result['upcoming_count'],
    }
