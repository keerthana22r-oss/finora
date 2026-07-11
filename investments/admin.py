from django.contrib import admin
from .models import Investment


@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'investment_type', 'amount_invested', 'current_value', 'date']
    list_filter = ['investment_type', 'user']
    search_fields = ['name']
