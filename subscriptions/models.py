from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal
from datetime import date
from dateutil.relativedelta import relativedelta

from transactions.models import ExpenseCategory


class Subscription(models.Model):
    BILLING_CYCLE_CHOICES = [
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    service_name = models.CharField(max_length=100)
    amount = models.DecimalField(
        max_digits=12, decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    billing_cycle = models.CharField(max_length=20, choices=BILLING_CYCLE_CHOICES, default='monthly')
    start_date = models.DateField()
    category = models.ForeignKey(ExpenseCategory, on_delete=models.PROTECT, related_name='subscriptions')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['service_name']

    def __str__(self):
        return f"{self.service_name} - ₹{self.amount}/{self.billing_cycle}"

    def get_next_payment_date(self, reference_date=None):
        """
        Calculated dynamically rather than stored — walks forward from
        start_date by the billing cycle interval until it reaches a date
        that's today (or the given reference_date) or later.
        This means the "next payment" is always correct even if the user
        hasn't opened the app in a while, without needing a scheduled job
        to update a stored field.
        """
        if reference_date is None:
            reference_date = date.today()

        interval_map = {
            'weekly': relativedelta(weeks=1),
            'monthly': relativedelta(months=1),
            'quarterly': relativedelta(months=3),
            'yearly': relativedelta(years=1),
        }
        interval = interval_map[self.billing_cycle]

        next_date = self.start_date
        # Safety cap at 1000 iterations so a bad date can never hang the request
        for _ in range(1000):
            if next_date >= reference_date:
                return next_date
            next_date += interval
        return next_date

    def get_monthly_equivalent_cost(self):
        """
        Normalizes any billing cycle into an equivalent monthly cost,
        so subscriptions on different cycles can be compared/summed fairly.
        Weekly uses 4.345 (average weeks per month) rather than a flat 4,
        since 4x would understate the true monthly cost.
        """
        conversions = {
            'weekly': self.amount * Decimal('4.345'),
            'monthly': self.amount,
            'quarterly': self.amount / Decimal('3'),
            'yearly': self.amount / Decimal('12'),
        }
        return conversions[self.billing_cycle]

    def get_annual_cost(self):
        return self.get_monthly_equivalent_cost() * 12
