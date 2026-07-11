from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Subscription
from .forms import SubscriptionForm
from . import services


@login_required
def subscription_list(request):
    overview = services.get_subscription_overview(request.user)
    inactive_subs = Subscription.objects.filter(user=request.user, is_active=False).select_related('category')
    return render(request, 'subscriptions/subscription_list.html', {
        'overview': overview,
        'inactive_subs': inactive_subs,
    })


@login_required
def subscription_add(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST, user=request.user)
        if form.is_valid():
            sub = form.save(commit=False)
            sub.user = request.user
            sub.save()
            messages.success(request, f'"{sub.service_name}" added.')
            return redirect('subscriptions:subscription_list')
    else:
        form = SubscriptionForm(user=request.user)
    return render(request, 'subscriptions/subscription_form.html', {'form': form, 'action': 'Add'})


@login_required
def subscription_edit(request, pk):
    sub = get_object_or_404(Subscription, pk=pk, user=request.user)
    if request.method == 'POST':
        form = SubscriptionForm(request.POST, instance=sub, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subscription updated.')
            return redirect('subscriptions:subscription_list')
    else:
        form = SubscriptionForm(instance=sub, user=request.user)
    return render(request, 'subscriptions/subscription_form.html', {'form': form, 'action': 'Edit'})


@login_required
def subscription_delete(request, pk):
    sub = get_object_or_404(Subscription, pk=pk, user=request.user)
    if request.method == 'POST':
        sub.delete()
        messages.success(request, 'Subscription deleted.')
        return redirect('subscriptions:subscription_list')
    return render(request, 'subscriptions/subscription_confirm_delete.html', {'subscription': sub})


@login_required
def subscription_toggle_active(request, pk):
    """
    Quick action to mark a subscription active/inactive without deleting it —
    cancelling Netflix shouldn't erase the fact you once tracked it.
    Only accepts POST to avoid a GET request accidentally toggling state.
    """
    sub = get_object_or_404(Subscription, pk=pk, user=request.user)
    if request.method == 'POST':
        sub.is_active = not sub.is_active
        sub.save()
        status = 'reactivated' if sub.is_active else 'marked inactive'
        messages.success(request, f'"{sub.service_name}" {status}.')
    return redirect('subscriptions:subscription_list')
