from django.contrib import admin
from .models import ExpenseCategory, Income, Expense, Budget


@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'icon']
    list_filter = ['user']
    search_fields = ['name']


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ['user', 'source', 'amount', 'date']
    list_filter = ['source', 'date', 'user']
    search_fields = ['description']
    date_hierarchy = 'date'


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['user', 'category', 'amount', 'date', 'payment_method']
    list_filter = ['category', 'payment_method', 'date', 'user']
    search_fields = ['description']
    date_hierarchy = 'date'


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ['user', 'category', 'month', 'year', 'limit_amount']
    list_filter = ['year', 'month', 'user']
    search_fields = ['category__name']
