import uuid

import django.contrib.auth.models
from ckeditor.fields import RichTextField
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

RESOURCE_TYPE_CHOICES = (
    ("Unsorted", (
        ("calendar", "Calendar"),
        ("campaign", "Campaign")
    )),
)


# Create your models here.
class AfterlineUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True,
                                to_field='username')


class AfterlineOwnedResource(models.Model):
    resource_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(AfterlineUser, on_delete=models.CASCADE, null=True, blank=True)
    resource_type = models.TextField(choices=RESOURCE_TYPE_CHOICES)


class Campaign(models.Model):
    title = models.CharField(max_length=200)
    game_master = models.ForeignKey(AfterlineUser, on_delete=models.CASCADE)
    description = RichTextField()
    public = models.BooleanField(default=False)

    resource = models.ForeignKey(AfterlineOwnedResource, on_delete=models.CASCADE, null=True)


class Player(models.Model):
    user = models.ForeignKey(AfterlineUser, on_delete=models.CASCADE)
    game = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [["user", "game"]]


class MessageNotification(models.Model):
    receiver = models.ForeignKey(AfterlineUser, related_name="MessageNotification_receiver", on_delete=models.CASCADE)
    sender = models.ForeignKey(AfterlineUser, related_name="MessageNotification_sender", on_delete=models.CASCADE,
                               null=True, blank=True)
    message = RichTextField()
    date_sent = models.DateTimeField(auto_now=True)
    viewed = models.BooleanField(default=False)


class CampaignInvite(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    receiver = models.ForeignKey(AfterlineUser, on_delete=models.CASCADE)
    date_sent = models.DateTimeField(auto_now=True)
    viewed = models.BooleanField(default=False)


class CampaignJoinRequest(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    sender = models.ForeignKey(AfterlineUser, on_delete=models.CASCADE)
    date_sent = models.DateTimeField(auto_now=True)
    viewed = models.BooleanField(default=False)


class AfterlinePermission(models.Model):
    perm = models.OneToOneField(django.contrib.auth.models.Permission, primary_key=True, on_delete=models.CASCADE)
    manager = models.ForeignKey(AfterlineUser, on_delete=models.CASCADE)


class Calendar(models.Model):
    title = models.CharField(max_length=200)
    view_perm = models.ForeignKey(AfterlinePermission, related_name="Calendar_view", on_delete=models.SET_NULL,
                                  null=True, blank=True)
    edit_perm = models.ForeignKey(AfterlinePermission, related_name="Calendar_edit", on_delete=models.SET_NULL,
                                  null=True, blank=True)

    resource = models.ForeignKey(AfterlineOwnedResource, on_delete=models.CASCADE, null=True)

    class Meta2:
        is_af_resource = True


class ResourceOwnershipTransferNotification(models.Model):
    resource = models.ForeignKey(AfterlineOwnedResource, on_delete=models.CASCADE)
    sender = models.ForeignKey(AfterlineUser, related_name="ResourceOwnershipTransferNotification_sender",
                               on_delete=models.CASCADE)
    receiver = models.ForeignKey(AfterlineUser, related_name="ResourceOwnershipTransferNotification_receiver",
                                 on_delete=models.CASCADE)
    date_sent = models.DateTimeField(auto_now=True)
    viewed = models.BooleanField(default=False)


@receiver(post_save, sender=User)
def post_save_user(sender, instance, **kwargs):
    if not AfterlineUser.objects.filter(user=instance).exists():
        AfterlineUser.objects.create(user=instance)
        print(f"Created AfterlineUser for {instance}")
