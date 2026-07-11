from django import forms
from decimal import Decimal
from .models import SavingsGoal


class SavingsGoalForm(forms.ModelForm):
    """
    Note: current_amount is intentionally NOT included here.
    New goals always start at ₹0 saved; existing goals get their
    current_amount changed only through AddFundsForm below —
    keeps "how much have I saved" separate from "what's the goal."
    """
    class Meta:
        model = SavingsGoal
        fields = ['name', 'target_amount', 'target_date', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Emergency Fund'}),
            'target_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01'}),
            'target_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Optional note'}),
        }


class AddFundsForm(forms.Form):
    """A tiny standalone form — just an amount to add to current_amount."""
    amount = forms.DecimalField(
        max_digits=12, decimal_places=2,
        min_value=Decimal('0.01'),
        widget=forms.NumberInput(attrs={
            'class': 'form-control', 'step': '0.01', 'min': '0.01', 'autofocus': True
        }),
        label='Amount to add'
    )
