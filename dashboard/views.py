from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def home_view(request):
    """
    Placeholder dashboard for Phase 1.
    Real summary cards, charts, and calculations get built in Phase 3
    once Income/Expense models exist (Phase 2).
    """
    return render(request, 'dashboard/home.html')
