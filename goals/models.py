from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal


class SavingsGoal(models.Model):
    """
    Unlike Budget (where actual spending is calculated live from Expense
    records), current_amount here IS stored directly — savings goals
    represent money the user is manually setting aside, tracked via the
    'Add Funds' action rather than derived from other models.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='savings_goals')
    name = models.CharField(max_length=100)
    target_amount = models.DecimalField(
        max_digits=12, decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    current_amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    target_date = models.DateField()
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['target_date']

    def __str__(self):
        return f"{self.name} - ₹{self.current_amount}/₹{self.target_amount}"
