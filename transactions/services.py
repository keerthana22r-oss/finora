from decimal import Decimal
from django.db.models import Sum
from .models import Budget, Expense
from dashboard.services import get_month_bounds


def get_budget_status(budget):
    """
    Compares one Budget against actual Expense records for that
    category/month/year. Returns a dict with everything the template needs.

    Warning tiers (per the project spec):
      - under 80%: normal (no warning)
      - 80-99%:    caution (approaching limit)
      - exactly 100% or slightly over: at limit
      - over 100%: exceeded
    """
    first_day, last_day = get_month_bounds(budget.year, budget.month)

    actual_spent = Expense.objects.filter(
        user=budget.user,
        category=budget.category,
        date__gte=first_day,
        date__lte=last_day,
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0')

    remaining = budget.limit_amount - actual_spent

    # Defensive: avoid ZeroDivisionError if limit_amount is somehow 0
    if budget.limit_amount > 0:
        percentage = (actual_spent / budget.limit_amount) * 100
    else:
        percentage = Decimal('0')

    if percentage >= 100:
        status = 'exceeded'
        status_label = 'Exceeded'
        status_color = 'danger'
    elif percentage >= 80:
        status = 'caution'
        status_label = 'Approaching Limit'
        status_color = 'warning'
    else:
        status = 'ok'
        status_label = 'On Track'
        status_color = 'success'

    return {
        'budget': budget,
        'actual_spent': actual_spent,
        'remaining': remaining,
        'percentage': min(percentage, Decimal('100')),  # cap the progress bar visual at 100%
        'raw_percentage': percentage,  # uncapped, for display text like "142% used"
        'status': status,
        'status_label': status_label,
        'status_color': status_color,
    }


def get_budgets_for_month(user, year, month):
    """Returns a list of budget-status dicts for every budget the user has in a given month."""
    budgets = Budget.objects.filter(user=user, year=year, month=month).select_related('category')
    return [get_budget_status(b) for b in budgets]
