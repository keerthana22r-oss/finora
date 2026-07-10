from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from itertools import chain
from operator import attrgetter

from .models import Income, Expense, ExpenseCategory
from .forms import IncomeForm, ExpenseForm


# ---------- INCOME VIEWS ----------

@login_required
def income_list(request):
    """
    Shows only the logged-in user's income records.
    request.user filtering here is what keeps data private between users.
    """
    incomes = Income.objects.filter(user=request.user)

    # Optional filters via query params: ?source=salary&date_from=2026-01-01&date_to=2026-01-31
    source = request.GET.get('source')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')

    if source:
        incomes = incomes.filter(source=source)
    if date_from:
        incomes = incomes.filter(date__gte=date_from)
    if date_to:
        incomes = incomes.filter(date__lte=date_to)

    total = sum(i.amount for i in incomes)

    return render(request, 'transactions/income_list.html', {
        'incomes': incomes,
        'total': total,
        'source_choices': Income.SOURCE_CHOICES,
    })


@login_required
def income_add(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user  # set server-side, never trust a hidden form field
            income.save()
            messages.success(request, 'Income added successfully.')
            return redirect('transactions:income_list')
    else:
        form = IncomeForm()
    return render(request, 'transactions/income_form.html', {'form': form, 'action': 'Add'})


@login_required
def income_edit(request, pk):
    # get_object_or_404 filtered by user=request.user means: if this income
    # belongs to someone else, Django returns a 404 instead of leaking it.
    income = get_object_or_404(Income, pk=pk, user=request.user)
    if request.method == 'POST':
        form = IncomeForm(request.POST, instance=income)
        if form.is_valid():
            form.save()
            messages.success(request, 'Income updated successfully.')
            return redirect('transactions:income_list')
    else:
        form = IncomeForm(instance=income)
    return render(request, 'transactions/income_form.html', {'form': form, 'action': 'Edit'})


@login_required
def income_delete(request, pk):
    income = get_object_or_404(Income, pk=pk, user=request.user)
    if request.method == 'POST':
        income.delete()
        messages.success(request, 'Income deleted.')
        return redirect('transactions:income_list')
    return render(request, 'transactions/income_confirm_delete.html', {'income': income})


# ---------- EXPENSE VIEWS ----------

@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user).select_related('category')

    category_id = request.GET.get('category')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')

    if category_id:
        expenses = expenses.filter(category_id=category_id)
    if date_from:
        expenses = expenses.filter(date__gte=date_from)
    if date_to:
        expenses = expenses.filter(date__lte=date_to)

    total = sum(e.amount for e in expenses)
    categories = ExpenseCategory.objects.filter(user=request.user)

    return render(request, 'transactions/expense_list.html', {
        'expenses': expenses,
        'total': total,
        'categories': categories,
    })


@login_required
def expense_add(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST, user=request.user)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            messages.success(request, 'Expense added successfully.')
            return redirect('transactions:expense_list')
    else:
        form = ExpenseForm(user=request.user)
    return render(request, 'transactions/expense_form.html', {'form': form, 'action': 'Add'})


@login_required
def expense_edit(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Expense updated successfully.')
            return redirect('transactions:expense_list')
    else:
        form = ExpenseForm(instance=expense, user=request.user)
    return render(request, 'transactions/expense_form.html', {'form': form, 'action': 'Edit'})


@login_required
def expense_delete(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        expense.delete()
        messages.success(request, 'Expense deleted.')
        return redirect('transactions:expense_list')
    return render(request, 'transactions/expense_confirm_delete.html', {'expense': expense})


# ---------- COMBINED TRANSACTION HISTORY ----------

@login_required
def transaction_history(request):
    """
    Combines Income and Expense into one chronological feed.
    We tag each record with a `txn_type` attribute so the template
    can tell them apart and style/link them differently.
    """
    incomes = Income.objects.filter(user=request.user)
    expenses = Expense.objects.filter(user=request.user).select_related('category')

    for i in incomes:
        i.txn_type = 'income'
    for e in expenses:
        e.txn_type = 'expense'

    combined = sorted(
        chain(incomes, expenses),
        key=attrgetter('date'),
        reverse=True
    )

    return render(request, 'transactions/transaction_history.html', {
        'transactions': combined,
    })
