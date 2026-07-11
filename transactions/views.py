from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from itertools import chain
from operator import attrgetter

from .models import Income, Expense, ExpenseCategory, Budget
from .forms import IncomeForm, ExpenseForm, BudgetForm, MONTH_CHOICES
from . import services as budget_services


# ---------- INCOME VIEWS ----------

@login_required
def income_list(request):
    incomes = Income.objects.filter(user=request.user)

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
            income.user = request.user
            income.save()
            messages.success(request, 'Income added successfully.')
            return redirect('transactions:income_list')
    else:
        form = IncomeForm()
    return render(request, 'transactions/income_form.html', {'form': form, 'action': 'Add'})


@login_required
def income_edit(request, pk):
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
    incomes = Income.objects.filter(user=request.user)
    expenses = Expense.objects.filter(user=request.user).select_related('category')

    for i in incomes:
        i.txn_type = 'income'
    for e in expenses:
        e.txn_type = 'expense'

    combined = sorted(chain(incomes, expenses), key=attrgetter('date'), reverse=True)

    return render(request, 'transactions/transaction_history.html', {'transactions': combined})


# ---------- BUDGET VIEWS ----------

@login_required
def budget_list(request):
    """
    Shows all budgets for a given month/year (default: current month),
    each with live-calculated actual spending, remaining amount, and
    warning status (see transactions/services.py for the math).
    """
    today = date.today()
    try:
        year = int(request.GET.get('year', today.year))
        month = int(request.GET.get('month', today.month))
        if month < 1 or month > 12:
            month = today.month
    except (ValueError, TypeError):
        year, month = today.year, today.month

    budget_statuses = budget_services.get_budgets_for_month(request.user, year, month)
    year_options = list(range(today.year - 3, today.year + 1))

    return render(request, 'transactions/budget_list.html', {
        'budget_statuses': budget_statuses,
        'selected_month': month,
        'selected_year': year,
        'month_choices': MONTH_CHOICES,
        'year_options': year_options,
    })


@login_required
def budget_add(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST, user=request.user)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            messages.success(request, 'Budget created successfully.')
            return redirect('transactions:budget_list')
    else:
        form = BudgetForm(user=request.user)
    return render(request, 'transactions/budget_form.html', {'form': form, 'action': 'Add'})


@login_required
def budget_edit(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=budget, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Budget updated successfully.')
            return redirect('transactions:budget_list')
    else:
        form = BudgetForm(instance=budget, user=request.user)
    return render(request, 'transactions/budget_form.html', {'form': form, 'action': 'Edit'})


@login_required
def budget_delete(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    if request.method == 'POST':
        budget.delete()
        messages.success(request, 'Budget deleted.')
        return redirect('transactions:budget_list')
    return render(request, 'transactions/budget_confirm_delete.html', {'budget': budget})
