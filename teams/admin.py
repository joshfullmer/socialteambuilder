from django.contrib import admin

from . import models


# Register your models here.
class PositionAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Position, PositionAdmin)
