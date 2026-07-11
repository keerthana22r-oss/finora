from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal


class ExpenseCategory(models.Model):
    """
    Categories are scoped per-user (not global) so users could eventually
    add their own custom categories. New users get the default set
    auto-created via a signal (see transactions/signals.py).
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expense_categories')
    name = models.CharField(max_length=50)
    icon = models.CharField(max_length=30, default='bi-tag', help_text="Bootstrap Icons class name")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        unique_together = ('user', 'name')  # prevents duplicate category names per user
        verbose_name_plural = 'Expense Categories'

    def __str__(self):
        return self.name


class Income(models.Model):
    SOURCE_CHOICES = [
        ('salary', 'Salary'),
        ('freelance', 'Freelance'),
        ('rental', 'Rental Income'),
        ('business', 'Business'),
        ('gift', 'Gift'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='incomes')
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES)
    amount = models.DecimalField(
        max_digits=12, decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    date = models.DateField()
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.get_source_display()} - ₹{self.amount} ({self.date})"


class Expense(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('debit_card', 'Debit Card'),
        ('credit_card', 'Credit Card'),
        ('upi', 'UPI'),
        ('net_banking', 'Net Banking'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    category = models.ForeignKey(
        ExpenseCategory, on_delete=models.PROTECT, related_name='expenses'
    )
    amount = models.DecimalField(
        max_digits=12, decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    date = models.DateField()
    description = models.CharField(max_length=255, blank=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='upi')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.category.name} - ₹{self.amount} ({self.date})"


class Budget(models.Model):
    """
    A spending limit for one category in one specific month.
    unique_together prevents duplicate budgets for the same
    (user, category, month, year) combination — edit the existing
    one instead of creating a second budget for the same period.
    Actual spending is NOT stored here; it's calculated live from
    Expense records in transactions/services.py, so it never goes stale.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE, related_name='budgets')
    month = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    year = models.IntegerField(validators=[MinValueValidator(2020), MaxValueValidator(2100)])
    limit_amount = models.DecimalField(
        max_digits=12, decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-year', '-month', 'category__name']
        unique_together = ('user', 'category', 'month', 'year')

    def __str__(self):
        return f"{self.category.name} budget - ₹{self.limit_amount} ({self.month}/{self.year})"
