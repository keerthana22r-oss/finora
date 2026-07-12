from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('reports/', views.reports_view, name='reports_home'),
    path('reports/export/csv/', views.export_csv, name='export_csv'),
    path('reports/export/pdf/', views.export_pdf, name='export_pdf'),
]
