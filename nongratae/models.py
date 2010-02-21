from django.db import models
from django.core.cache import cathe
from django.contrib.sites.models import Site
from django.conf import settings

from nongratae.constants import BLOCKED_IPS_CACHE_KEY

BLOCKED_IPS_CACHE_KEY = BLOCKED_IPS_CACHE_KEY % settings.SITE_ID

class BlockedIp(models.Model):
    """ Represents a Blocked IP that isn't welcome to the site """
    site = models.ForeignKey(Site)
    ip = models.IPField()
    motive = models.CharField(max_length=256)
    date_blocked = models.DateField(auto_now=True)


    def save(self, *args, **kwargs):
        """ Overriden to clear Cache after a new IP is added """
        cache.delete(BLOCKED_IPS_CACHE_KEY)
        super(BlockedIP, self).save(*args, **kwargs)
