from django.contrib import admin

# Register your models here.
from .models import Device, DeviceData

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ("name", "nonce", "assoc", "created", "modified")
    list_filter = ("created", "modified" )
    search_fields = ("name__startswith", )

    class Meta:
        ordering = ("modified","created")


@admin.register(DeviceData)
class DeviceDataAdmin(admin.ModelAdmin):
    list_display = ("ip", "mac", "mq135", "ordate", "redate")
    list_filter = ("mac", "ordate", "redate" )
    search_fields = ("mac__startswith", )

    class Meta:
        ordering = ("ordate", "redate")