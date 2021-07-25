from django.db import models
from django.utils import timezone
from django.forms import model_to_dict
import datetime

# Create your models here.
class Device(models.Model):
    name = models.CharField(max_length=33)
    nonce = models.CharField(max_length=33)
    assoc = models.CharField(max_length=128, default="NONE")
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField(editable=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.created:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Device, self).save(*args, **kwargs)

    #RETORNAR OBJETO EN  JSON
    def toJSON(self):
        item = model_to_dict(self)
        item['created'] =  self.created.strftime('%Y/%m/%d %H:%M')
        item['modified'] =  self.modified.strftime('%Y/%m/%d %H:%M')
        return item

class DeviceData(models.Model):
    ip = models.CharField(max_length=16)
    mac = models.CharField(max_length=13)
    mq135 = models.CharField(max_length=128, default="NONE")
    sds011 = models.CharField(max_length=128, default="NONE")
    ordate = models.DateTimeField(editable=False)
    redate = models.DateTimeField(editable=False)

    def __str__(self):
        return self.mac + "|" + self.mac

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.redate:
            self.redate = timezone.now()
        return super(DeviceData, self).save(*args, **kwargs)

    #RETORNAR OBJETO EN  JSON
    def toJSON(self):
        item = model_to_dict(self)
        item['ordate'] =  self.ordate.strftime('%Y/%m/%d %H:%M')
        item['redate'] =  self.redate.strftime('%Y/%m/%d %H:%M')
        return item