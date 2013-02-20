from django.db import models
from datetime import datetime

class Account(models.Model):
    fa          = models.CharField(max_length=200)
    weasyl      = models.CharField(max_length=200)
    vouchers    = models.IntegerField(default=0)
    ip          = models.IPAddressField(default="")
    
    def __unicode__(self):
        return "An Account Class"

class Voucher(models.Model):
    ip          = models.IPAddressField(default="")
    fa_id       = models.IntegerField(default=0)
    timestamp   = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return "Voucher for an account"