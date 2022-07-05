from django.contrib import admin

from . import models

# Register your models here.

admin.site.register(models.AfterlineUser)
admin.site.register(models.Campaign)
admin.site.register(models.Player)
admin.site.register(models.MessageNotification)
admin.site.register(models.CampaignInvite)
admin.site.register(models.CampaignJoinRequest)
admin.site.register(models.AfterlinePermission)
admin.site.register(models.AfterlineOwnedResource)
admin.site.register(models.Calendar)
admin.site.register(models.ResourceOwnershipTransferNotification)




