import uuid
from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import User

# Create your models here.
class AfterlineUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True, to_field='username')
    


@receiver(post_save, sender=User)
def post_save_user(sender, instance, **kwargs):
    if not AfterlineUser.objects.filter(user=instance).exists():
        AfterlineUser.objects.create(user=instance)
        print(f"Created AfterlineUser for {instance}")

