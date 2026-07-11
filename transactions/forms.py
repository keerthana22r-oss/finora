from django import forms
from datetime import date
from .models import Income, Expense, ExpenseCategory, Budget


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['source', 'amount', 'date', 'description']
        widgets = {
            'source': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional note'}),
        }


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'amount', 'date', 'payment_method', 'description']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'payment_method': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional note'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['category'].queryset = ExpenseCategory.objects.filter(user=user)


MONTH_CHOICES = [
    (1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'),
    (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'),
    (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December'),
]


class BudgetForm(forms.ModelForm):
    month = forms.ChoiceField(choices=MONTH_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = Budget
        fields = ['category', 'month', 'year', 'limit_amount']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'year': forms.NumberInput(attrs={'class': 'form-control', 'min': '2020', 'max': '2100'}),
            'limit_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        # Same pattern as ExpenseForm: restrict category choices to this user's own categories.
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.user = user
        if user is not None:
            self.fields['category'].queryset = ExpenseCategory.objects.filter(user=user)
        if not self.instance.pk:
            # Sensible defaults for a brand-new budget: current month/year
            today = date.today()
            self.fields['month'].initial = today.month
            self.fields['year'].initial = today.year

    def clean(self):
        # Extra safety net: unique_together already enforces this at the DB level,
        # but catching it here lets us show a friendly error instead of a raw
        # IntegrityError page if somehow a duplicate slips through.
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        month = cleaned_data.get('month')
        year = cleaned_data.get('year')

        if category and month and year and self.user:
            existing = Budget.objects.filter(
                user=self.user, category=category, month=month, year=year
            ).exclude(pk=self.instance.pk)
            if existing.exists():
                raise forms.ValidationError(
                    f'A budget for {category.name} in {dict(MONTH_CHOICES)[int(month)]} {year} already exists. '
                    'Edit that one instead.'
                )
        return cleaned_data
