from django.contrib import admin
from .models import Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['service_name', 'user', 'amount', 'billing_cycle', 'is_active']
    list_filter = ['billing_cycle', 'is_active', 'user']
    search_fields = ['service_name']
