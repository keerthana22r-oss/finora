from decimal import Decimal
from dateutil.relativedelta import relativedelta
from django.db.models import Sum

from transactions.models import Expense, Income
from dashboard.services import get_month_bounds, get_summary_data


def get_category_change_insights(user, year, month, threshold_pct=15):
    """
    Compares this month's spending per category against last month's.
    Flags categories that moved by threshold_pct% or more, in either
    direction. Requires last month's amount to be non-zero to avoid
    a meaningless "infinite % increase" from ₹0.
    """
    this_first, this_last = get_month_bounds(year, month)
    prev_date = get_month_bounds(year, month)[0] - relativedelta(months=1)
    prev_first, prev_last = get_month_bounds(prev_date.year, prev_date.month)

    this_month_totals = dict(
        Expense.objects.filter(user=user, date__gte=this_first, date__lte=this_last)
        .values_list('category__name')
        .annotate(total=Sum('amount'))
        .values_list('category__name', 'total')
    )
    prev_month_totals = dict(
        Expense.objects.filter(user=user, date__gte=prev_first, date__lte=prev_last)
        .values_list('category__name')
        .annotate(total=Sum('amount'))
        .values_list('category__name', 'total')
    )

    insights = []
    for category, prev_amount in prev_month_totals.items():
        if not prev_amount or prev_amount == 0:
            continue
        this_amount = this_month_totals.get(category, Decimal('0'))
        change_pct = ((this_amount - prev_amount) / prev_amount) * 100

        if abs(change_pct) >= threshold_pct:
            direction = 'increased' if change_pct > 0 else 'decreased'
            color = 'danger' if change_pct > 0 else 'success'
            icon = 'bi-arrow-up-circle' if change_pct > 0 else 'bi-arrow-down-circle'
            insights.append({
                'icon': icon,
                'color': color,
                'message': f"Your {category} spending {direction} by {abs(change_pct):.0f}% compared with last month.",
            })

    return insights


def get_top_category_insight(user, year, month):
    summary = get_summary_data(user, year, month)
    if summary['top_category_name']:
        return {
            'icon': 'bi-trophy',
            'color': 'info',
            'message': f"{summary['top_category_name']} is your highest spending category this month, at ₹{summary['top_category_amount']:,.2f}.",
        }
    return None


def get_budget_insights(user, year, month):
    """Reuses the Phase 4 budget calculation logic to surface warnings as plain-language insights."""
    from transactions.services import get_budgets_for_month

    insights = []
    for item in get_budgets_for_month(user, year, month):
        if item['status'] == 'exceeded':
            insights.append({
                'icon': 'bi-exclamation-octagon-fill',
                'color': 'danger',
                'message': f"You've exceeded your {item['budget'].category.name} budget by ₹{abs(item['remaining']):,.2f} this month.",
            })
        elif item['status'] == 'caution':
            insights.append({
                'icon': 'bi-exclamation-triangle-fill',
                'color': 'warning',
                'message': f"You've used {item['raw_percentage']:.0f}% of your {item['budget'].category.name} budget this month.",
            })
    return insights


def get_subscription_insight(user):
    """Reuses the Phase 6 subscription calculation logic."""
    from subscriptions.services import get_subscription_overview

    overview = get_subscription_overview(user)
    if overview['active_count'] > 0:
        return {
            'icon': 'bi-arrow-repeat',
            'color': 'info',
            'message': f"Your subscriptions cost ₹{overview['total_monthly']:,.2f} per month across {overview['active_count']} active subscription{'s' if overview['active_count'] != 1 else ''}.",
        }
    return None


def get_savings_rate_insight(user, year, month):
    """
    Compares this month's savings rate (surplus ÷ income, as a %) against
    last month's. Requires income > 0 in both months to produce a
    meaningful rate — otherwise the comparison is skipped entirely.
    """
    this_summary = get_summary_data(user, year, month)

    prev_date = get_month_bounds(year, month)[0] - relativedelta(months=1)
    prev_summary = get_summary_data(user, prev_date.year, prev_date.month)

    if this_summary['total_income'] <= 0 or prev_summary['total_income'] <= 0:
        return None

    this_rate = (this_summary['surplus_deficit'] / this_summary['total_income']) * 100
    prev_rate = (prev_summary['surplus_deficit'] / prev_summary['total_income']) * 100

    diff = this_rate - prev_rate
    if abs(diff) < 1:
        return None  # not a meaningful enough change to mention

    if diff > 0:
        return {
            'icon': 'bi-graph-up',
            'color': 'success',
            'message': f"Your savings rate improved to {this_rate:.0f}% this month, up from {prev_rate:.0f}% last month.",
        }
    else:
        return {
            'icon': 'bi-graph-down',
            'color': 'warning',
            'message': f"Your savings rate dropped to {this_rate:.0f}% this month, down from {prev_rate:.0f}% last month.",
        }


def get_goal_projection_insights(user, months_to_average=3):
    """
    For each active (incomplete, not overdue) savings goal, estimates
    months-to-completion based on the user's ACTUAL average monthly
    savings over the last few months — different from Phase 5's
    "required pace to hit the target date," this is "the pace you're
    actually on track for right now."
    """
    from goals.models import SavingsGoal
    from goals.services import get_goal_progress
    from datetime import date

    today = date.today()
    total_savings = Decimal('0')
    for i in range(months_to_average):
        target = today.replace(day=1) - relativedelta(months=i)
        summary = get_summary_data(user, target.year, target.month)
        total_savings += summary['surplus_deficit']

    avg_monthly_savings = total_savings / months_to_average

    insights = []
    if avg_monthly_savings > 0:
        goals = SavingsGoal.objects.filter(user=user)
        for goal in goals:
            status = get_goal_progress(goal)
            if status['is_completed'] or status['is_overdue']:
                continue
            months_needed = status['remaining_amount'] / avg_monthly_savings
            insights.append({
                'icon': 'bi-flag',
                'color': 'info',
                'message': f"At your current average saving rate of ₹{avg_monthly_savings:,.2f}/month, "
                           f"you may reach \"{goal.name}\" in approximately {months_needed:.0f} months.",
            })
    return insights


def generate_insights(user, year, month):
    """
    Combines all rule-based insights into one ordered list for the
    Insights page. Order is intentional: budget warnings and category
    spikes first (most actionable), then positive/neutral summaries.
    """
    insights = []

    insights.extend(get_budget_insights(user, year, month))
    insights.extend(get_category_change_insights(user, year, month))

    top_category = get_top_category_insight(user, year, month)
    if top_category:
        insights.append(top_category)

    savings_rate = get_savings_rate_insight(user, year, month)
    if savings_rate:
        insights.append(savings_rate)

    subscription = get_subscription_insight(user)
    if subscription:
        insights.append(subscription)

    insights.extend(get_goal_projection_insights(user))

    return insights
