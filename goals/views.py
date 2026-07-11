from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import SavingsGoal
from .forms import SavingsGoalForm, AddFundsForm
from . import services


@login_required
def goal_list(request):
    goal_statuses = services.get_goals_overview(request.user)
    return render(request, 'goals/goal_list.html', {'goal_statuses': goal_statuses})


@login_required
def goal_add(request):
    if request.method == 'POST':
        form = SavingsGoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            messages.success(request, f'Goal "{goal.name}" created.')
            return redirect('goals:goal_list')
    else:
        form = SavingsGoalForm()
    return render(request, 'goals/goal_form.html', {'form': form, 'action': 'Add'})


@login_required
def goal_edit(request, pk):
    goal = get_object_or_404(SavingsGoal, pk=pk, user=request.user)
    if request.method == 'POST':
        form = SavingsGoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            messages.success(request, 'Goal updated successfully.')
            return redirect('goals:goal_list')
    else:
        form = SavingsGoalForm(instance=goal)
    return render(request, 'goals/goal_form.html', {'form': form, 'action': 'Edit'})


@login_required
def goal_delete(request, pk):
    goal = get_object_or_404(SavingsGoal, pk=pk, user=request.user)
    if request.method == 'POST':
        goal.delete()
        messages.success(request, 'Goal deleted.')
        return redirect('goals:goal_list')
    return render(request, 'goals/goal_confirm_delete.html', {'goal': goal})


@login_required
def goal_add_funds(request, pk):
    """
    Dedicated action for adding money to an existing goal.
    Kept separate from goal_edit so users aren't editing the whole
    goal (name/target/date) just to log a deposit.
    """
    goal = get_object_or_404(SavingsGoal, pk=pk, user=request.user)
    if request.method == 'POST':
        form = AddFundsForm(request.POST)
        if form.is_valid():
            goal.current_amount += form.cleaned_data['amount']
            goal.save()
            messages.success(request, f'Added ₹{form.cleaned_data["amount"]} to "{goal.name}".')
            return redirect('goals:goal_list')
    else:
        form = AddFundsForm()
    return render(request, 'goals/goal_add_funds.html', {'form': form, 'goal': goal})
