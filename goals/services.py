from datetime import date
from decimal import Decimal
from dateutil.relativedelta import relativedelta


def get_goal_progress(goal):
    """
    Returns progress percentage, remaining amount, months remaining until
    the target date, and the estimated monthly saving needed to hit it.

    Handles two edge cases explicitly:
      - target_amount is somehow 0 (avoid ZeroDivisionError)
      - target_date has already passed (avoid negative/zero month counts)
    """
    remaining_amount = goal.target_amount - goal.current_amount

    if goal.target_amount > 0:
        percentage = (goal.current_amount / goal.target_amount) * 100
    else:
        percentage = Decimal('0')

    today = date.today()
    is_completed = goal.current_amount >= goal.target_amount
    is_overdue = goal.target_date < today and not is_completed

    months_remaining = None
    monthly_required = None

    if not is_completed and not is_overdue:
        delta = relativedelta(goal.target_date, today)
        months_remaining = delta.years * 12 + delta.months
        # If less than a month remains but the date hasn't passed yet,
        # round up to 1 so we don't divide by zero.
        if months_remaining < 1:
            months_remaining = 1
        monthly_required = remaining_amount / months_remaining

    return {
        'goal': goal,
        'remaining_amount': remaining_amount,
        'percentage': min(percentage, Decimal('100')),
        'raw_percentage': percentage,
        'is_completed': is_completed,
        'is_overdue': is_overdue,
        'months_remaining': months_remaining,
        'monthly_required': monthly_required,
    }


def get_goals_overview(user):
    """List of progress dicts for every goal this user has, most urgent first."""
    from .models import SavingsGoal
    goals = SavingsGoal.objects.filter(user=user)
    return [get_goal_progress(g) for g in goals]
