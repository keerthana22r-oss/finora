from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import ExpenseCategory

DEFAULT_CATEGORIES = [
    ('Housing', 'bi-house-door'),
    ('Utilities', 'bi-lightning-charge'),
    ('Phone', 'bi-telephone'),
    ('Insurance', 'bi-shield-check'),
    ('Groceries', 'bi-cart'),
    ('Transport', 'bi-bus-front'),
    ('Health', 'bi-heart-pulse'),
    ('Gifts', 'bi-gift'),
    ('Eating Out', 'bi-cup-straw'),
    ('Shopping', 'bi-bag'),
    ('Travel', 'bi-airplane'),
    ('Subscriptions', 'bi-arrow-repeat'),
    ('Gym/Fitness', 'bi-heart'),
    ('Education', 'bi-book'),
    ('Entertainment', 'bi-film'),
    ('Other', 'bi-three-dots'),
]


@receiver(post_save, sender=User)
def create_default_categories(sender, instance, created, **kwargs):
    """
    Runs automatically when a new User is created.
    Seeds the 16 default expense categories for that user only.
    Uses get_or_create so re-running this never creates duplicates.
    """
    if created:
        for name, icon in DEFAULT_CATEGORIES:
            ExpenseCategory.objects.get_or_create(
                user=instance, name=name, defaults={'icon': icon}
            )
