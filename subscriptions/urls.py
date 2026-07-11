from django.urls import path
from . import views

app_name = 'subscriptions'

urlpatterns = [
    path('subscriptions/', views.subscription_list, name='subscription_list'),
    path('subscriptions/add/', views.subscription_add, name='subscription_add'),
    path('subscriptions/<int:pk>/edit/', views.subscription_edit, name='subscription_edit'),
    path('subscriptions/<int:pk>/delete/', views.subscription_delete, name='subscription_delete'),
    path('subscriptions/<int:pk>/toggle/', views.subscription_toggle_active, name='subscription_toggle'),
]
