from django.contrib import admin

# Register your models here.
from .models import Device

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ("name", "nonce", "assoc", "created", "modified")
    list_filter = ("created", "modified" )
    search_fields = ("name__startswith", )

    class Meta:
        ordering = ("modified","created")