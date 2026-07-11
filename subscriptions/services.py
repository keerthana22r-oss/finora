from datetime import date, timedelta
from decimal import Decimal
from .models import Subscription


def get_subscription_overview(user):
    """
    Returns active subscriptions with their calculated next payment date,
    sorted soonest-first, plus totals for the dashboard/list page.
    """
    active_subs = Subscription.objects.filter(user=user, is_active=True).select_related('category')

    sub_data = []
    total_monthly = Decimal('0')
    today = date.today()
    upcoming_cutoff = today + timedelta(days=7)
    upcoming_count = 0

    for sub in active_subs:
        next_payment = sub.get_next_payment_date()
        monthly_cost = sub.get_monthly_equivalent_cost()
        total_monthly += monthly_cost

        is_upcoming = today <= next_payment <= upcoming_cutoff
        if is_upcoming:
            upcoming_count += 1

        sub_data.append({
            'subscription': sub,
            'next_payment_date': next_payment,
            'monthly_cost': monthly_cost,
            'annual_cost': sub.get_annual_cost(),
            'is_upcoming': is_upcoming,
        })

    sub_data.sort(key=lambda x: x['next_payment_date'])

    return {
        'subscriptions': sub_data,
        'total_monthly': total_monthly,
        'total_annual': total_monthly * 12,
        'upcoming_count': upcoming_count,
        'active_count': active_subs.count(),
    }
