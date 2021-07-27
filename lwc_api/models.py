from django.db import models
from django.utils import timezone
from django.forms import model_to_dict
import datetime as dt

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
        #FORMATEAR FECHA A +5
        local_tz = dt.timezone(dt.timedelta(hours=+5))
        utc = dt.timezone.utc
        created = dt.datetime(self.created.year,self.created.month,self.created.day,self.created.hour,self.created.minute,self.created.second, 0, local_tz)
        modified = dt.datetime(self.modified.year,self.modified.month,self.modified.day,self.modified.hour,self.modified.minute,self.modified.second, 0, local_tz)

        item['created'] =  created.astimezone(utc)
        item['modified'] =  modified.astimezone(utc)
        
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
	#FORMATEAR FECHA A +5
        local_tz = dt.timezone(dt.timedelta(hours=+5))
        utc = dt.timezone.utc
        ordate = dt.datetime(self.ordate.year,self.ordate.month,self.ordate.day,self.ordate.hour,self.ordate.minute,self.ordate.second, 0, local_tz)
        redate = dt.datetime(self.redate.year,self.redate.month,self.redate.day,self.redate.hour,self.redate.minute,self.redate.second, 0, local_tz)
        #CAMBIAR FORMATO
        item['ordate'] =  ordate.astimezone(utc).strftime('%Y/%m/%d %H:%M')
        item['redate'] =  redate.astimezone(utc).strftime('%Y/%m/%d %H:%M')
        return item
