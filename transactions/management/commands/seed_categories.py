from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from transactions.models import ExpenseCategory
from transactions.signals import DEFAULT_CATEGORIES


class Command(BaseCommand):
    help = 'Seeds default expense categories for all existing users who don\'t have them yet'

    def handle(self, *args, **options):
        total_created = 0
        for user in User.objects.all():
            for name, icon in DEFAULT_CATEGORIES:
                obj, created = ExpenseCategory.objects.get_or_create(
                    user=user, name=name, defaults={'icon': icon}
                )
                if created:
                    total_created += 1
        self.stdout.write(self.style.SUCCESS(
            f'Done. Created {total_created} new category records across all users.'
        ))
