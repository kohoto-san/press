from django.contrib import admin
from hunt import models

admin.site.register(models.Profile)
admin.site.register(models.Post)
admin.site.register(models.Comment)
admin.site.register(models.Invite)
