from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal


class Investment(models.Model):
    """
    Manual investment tracking only — no live market data connections
    in this version, per the project spec. current_value is something
    the user updates themselves when they check their actual statements.
    Gain/loss is never stored here; it's calculated live in services.py
    from current_value - amount_invested, so it can never go stale.
    """
    INVESTMENT_TYPE_CHOICES = [
        ('stocks', 'Stocks'),
        ('mutual_funds', 'Mutual Funds'),
        ('fixed_deposit', 'Fixed Deposit'),
        ('real_estate', 'Real Estate'),
        ('gold', 'Gold'),
        ('crypto', 'Cryptocurrency'),
        ('ppf', 'PPF / EPF'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='investments')
    name = models.CharField(max_length=100, help_text="e.g. HDFC Bank shares, Axis Bluechip Fund")
    investment_type = models.CharField(max_length=20, choices=INVESTMENT_TYPE_CHOICES)
    amount_invested = models.DecimalField(
        max_digits=12, decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    current_value = models.DecimalField(
        max_digits=12, decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Update this whenever you check your latest statement"
    )
    date = models.DateField(help_text="Date of investment")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.name} - ₹{self.amount_invested} invested"
