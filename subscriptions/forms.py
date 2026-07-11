from django import forms
from .models import Subscription
from transactions.models import ExpenseCategory


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['service_name', 'amount', 'billing_cycle', 'start_date', 'category', 'is_active']
        widgets = {
            'service_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Netflix'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01'}),
            'billing_cycle': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        # Same pattern used throughout: restrict category choices to this user's own.
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['category'].queryset = ExpenseCategory.objects.filter(user=user)
