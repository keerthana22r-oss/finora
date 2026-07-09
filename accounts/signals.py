from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Runs automatically every time a User is saved.
    If the User was just created, also create their Profile.
    If the User already existed, just save the existing Profile (no-op safety).
    """
    if created:
        Profile.objects.create(user=instance)
    else:
        # Ensures older users (created before this signal existed) don't crash
        Profile.objects.get_or_create(user=instance)
