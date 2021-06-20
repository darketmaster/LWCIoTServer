from django.db import models
from django.utils import timezone

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
