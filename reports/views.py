import csv
from datetime import date
from io import BytesIO

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from . import services
from dashboard.services import get_category_breakdown_chart_data


MONTH_NAMES = [
    (1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'),
    (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'),
    (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December'),
]


def _get_selected_period(request):
    """Shared helper: reads ?year=&month= from the query string with safe defaults."""
    today = date.today()
    try:
        year = int(request.GET.get('year', today.year))
        month = int(request.GET.get('month', today.month))
        if month < 1 or month > 12:
            month = today.month
    except (ValueError, TypeError):
        year, month = today.year, today.month
    return year, month


@login_required
def reports_view(request):
    year, month = _get_selected_period(request)

    yearly_summary = services.get_yearly_summary(request.user, year)
    category_totals = services.get_category_totals_for_year(request.user, year)
    month_category_breakdown = get_category_breakdown_chart_data(request.user, year, month)

    from transactions.services import get_budgets_for_month
    budget_statuses = get_budgets_for_month(request.user, year, month)

    today = date.today()
    year_options = list(range(today.year - 3, today.year + 1))

    return render(request, 'reports/reports_home.html', {
        'yearly_summary': yearly_summary,
        'category_totals': category_totals,
        'month_category_breakdown': month_category_breakdown,
        'budget_statuses': budget_statuses,
        'selected_year': year,
        'selected_month': month,
        'month_names': MONTH_NAMES,
        'year_options': year_options,
        'selected_month_label': dict(MONTH_NAMES).get(month, ''),
    })


@login_required
def export_csv(request):
    """
    Exports the full year's transactions as a CSV file.
    Streams directly as a download rather than saving to disk first.
    """
    year, _ = _get_selected_period(request)
    transactions = services.get_transactions_for_year(request.user, year)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="wealthora_transactions_{year}.csv"'

    writer = csv.writer(response)
    writer.writerow(['Date', 'Type', 'Category / Source', 'Description', 'Amount (INR)'])
    for row in transactions:
        writer.writerow([
            row['date'].strftime('%d-%m-%Y'),
            row['type'],
            row['category_or_source'],
            row['description'],
            f"{row['amount']:.2f}",
        ])

    return response


@login_required
def export_pdf(request):
    """
    Exports a yearly summary PDF using ReportLab — a pure-Python PDF
    library with no native/system dependencies, which installs cleanly
    on Windows (unlike some alternatives that need extra system libraries).
    """
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet

    year, _ = _get_selected_period(request)
    yearly_summary = services.get_yearly_summary(request.user, year)

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=2 * cm, bottomMargin=2 * cm)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph(f"Wealthora — Financial Summary Report ({year})", styles['Title']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Prepared for: {request.user.username}", styles['Normal']))
    elements.append(Spacer(1, 20))

    # Summary totals
    elements.append(Paragraph("Yearly Totals", styles['Heading2']))
    totals_data = [
        ['Total Income', f"Rs. {yearly_summary['total_income']:,.2f}"],
        ['Total Expenses', f"Rs. {yearly_summary['total_expense']:,.2f}"],
        ['Net Surplus/Deficit', f"Rs. {yearly_summary['total_surplus']:,.2f}"],
    ]
    totals_table = Table(totals_data, colWidths=[8 * cm, 8 * cm])
    totals_table.setStyle(TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
    ]))
    elements.append(totals_table)
    elements.append(Spacer(1, 20))

    # Month-by-month table
    elements.append(Paragraph("Month-by-Month Breakdown", styles['Heading2']))
    table_data = [['Month', 'Income', 'Expenses', 'Surplus/Deficit']]
    for row in yearly_summary['rows']:
        table_data.append([
            row['month_name'],
            f"Rs. {row['income']:,.2f}",
            f"Rs. {row['expense']:,.2f}",
            f"Rs. {row['surplus_deficit']:,.2f}",
        ])

    monthly_table = Table(table_data, colWidths=[3 * cm, 4.5 * cm, 4.5 * cm, 4.5 * cm])
    monthly_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2f80ed')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f4f6f9')]),
    ]))
    elements.append(monthly_table)

    doc.build(elements)
    buffer.seek(0)

    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="wealthora_summary_{year}.pdf"'
    return response
