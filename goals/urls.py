from django.urls import path
from . import views

app_name = 'goals'

urlpatterns = [
    path('goals/', views.goal_list, name='goal_list'),
    path('goals/add/', views.goal_add, name='goal_add'),
    path('goals/<int:pk>/edit/', views.goal_edit, name='goal_edit'),
    path('goals/<int:pk>/delete/', views.goal_delete, name='goal_delete'),
    path('goals/<int:pk>/add-funds/', views.goal_add_funds, name='goal_add_funds'),
]
