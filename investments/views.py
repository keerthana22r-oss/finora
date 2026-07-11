from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Investment
from .forms import InvestmentForm
from . import services


@login_required
def investment_list(request):
    overview = services.get_portfolio_overview(request.user)
    return render(request, 'investments/investment_list.html', {'overview': overview})


@login_required
def investment_add(request):
    if request.method == 'POST':
        form = InvestmentForm(request.POST)
        if form.is_valid():
            investment = form.save(commit=False)
            investment.user = request.user
            investment.save()
            messages.success(request, f'"{investment.name}" added to your portfolio.')
            return redirect('investments:investment_list')
    else:
        form = InvestmentForm()
    return render(request, 'investments/investment_form.html', {'form': form, 'action': 'Add'})


@login_required
def investment_edit(request, pk):
    investment = get_object_or_404(Investment, pk=pk, user=request.user)
    if request.method == 'POST':
        form = InvestmentForm(request.POST, instance=investment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Investment updated. (Tip: update current_value here whenever you check your statement.)')
            return redirect('investments:investment_list')
    else:
        form = InvestmentForm(instance=investment)
    return render(request, 'investments/investment_form.html', {'form': form, 'action': 'Edit'})


@login_required
def investment_delete(request, pk):
    investment = get_object_or_404(Investment, pk=pk, user=request.user)
    if request.method == 'POST':
        investment.delete()
        messages.success(request, 'Investment removed.')
        return redirect('investments:investment_list')
    return render(request, 'investments/investment_confirm_delete.html', {'investment': investment})
