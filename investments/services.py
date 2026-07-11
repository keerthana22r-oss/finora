from decimal import Decimal
from django.db.models import Sum
from .models import Investment


def get_investment_status(investment):
    """
    Calculates gain/loss for one investment. Never stored on the model —
    always derived from current_value - amount_invested so it's
    impossible for this number to go stale after an edit.
    """
    gain_loss = investment.current_value - investment.amount_invested

    if investment.amount_invested > 0:
        gain_loss_percentage = (gain_loss / investment.amount_invested) * 100
    else:
        gain_loss_percentage = Decimal('0')

    return {
        'investment': investment,
        'gain_loss': gain_loss,
        'gain_loss_percentage': gain_loss_percentage,
        'is_gain': gain_loss >= 0,
    }


def get_portfolio_overview(user):
    """
    Aggregates every investment into portfolio-wide totals for the
    summary cards at the top of the Investments page.
    """
    investments = Investment.objects.filter(user=user)

    if not investments.exists():
        return {'has_investments': False}

    total_invested = investments.aggregate(total=Sum('amount_invested'))['total'] or Decimal('0')
    total_current_value = investments.aggregate(total=Sum('current_value'))['total'] or Decimal('0')
    total_gain_loss = total_current_value - total_invested

    if total_invested > 0:
        total_gain_loss_percentage = (total_gain_loss / total_invested) * 100
    else:
        total_gain_loss_percentage = Decimal('0')

    investment_statuses = [get_investment_status(inv) for inv in investments]

    return {
        'has_investments': True,
        'total_invested': total_invested,
        'total_current_value': total_current_value,
        'total_gain_loss': total_gain_loss,
        'total_gain_loss_percentage': total_gain_loss_percentage,
        'is_overall_gain': total_gain_loss >= 0,
        'investment_statuses': investment_statuses,
        'count': investments.count(),
    }
