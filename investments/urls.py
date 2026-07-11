from django.urls import path
from . import views

app_name = 'investments'

urlpatterns = [
    path('investments/', views.investment_list, name='investment_list'),
    path('investments/add/', views.investment_add, name='investment_add'),
    path('investments/<int:pk>/edit/', views.investment_edit, name='investment_edit'),
    path('investments/<int:pk>/delete/', views.investment_delete, name='investment_delete'),
]
