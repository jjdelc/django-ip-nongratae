# -~- coding: utf-8 -*-

from datetime import datetime

from django.db import models
from django.core.cache import cache
from django.contrib.sites.models import Site
from django.conf import settings

from nongratae.constants import BLOCKED_IPS_CACHE_KEY

BLOCKED_IPS_CACHE_KEY = BLOCKED_IPS_CACHE_KEY % settings.SITE_ID

class Visit(models.Model):
    """ Represents a Web Hit """
    ip = models.IPAddressField()
    referer = models.CharField(max_length=512, blank=True)
    user_agent = models.CharField(max_length=256, blank=True)
    method = models.CharField(max_length=8)
    accept_headers = models.CharField(max_length=64, blank=True)
    visit_time = models.DateTimeField()

    def build_from_request(self, request):
        """ Fills out the Visit fields based on the Request data """
        self.ip = request.META['REMOTE_ADDR']
        self.referer = request.META.get('HTTP_REFERER', '')
        self.user_agent = request.META.get('HTTP_USER_AGENT', '')
        self.method = request.META['REQUEST_METHOD']
        self.accept = request.META.get('HTTP_ACCEPT', '')
        self.visit_time = datetime.now()


class IPNonGrata(models.Model):
    """ Represents a Blocked IP that isn't welcome to the site """
    
    BLOCKED = 2
    SUSPICIOUS = 1
    CLEAN = 0

    IP_STATUS = (
        (CLEAN, u'Ip Clean'),
        (SUSPICIOUS, u'Ip Suspicious'),
        (BLOCKED, u'Ip Blocked'),
    )

    site = models.ForeignKey(Site)
    ip = models.IPAddressField()
    motive = models.CharField(max_length=256)
    date_blocked = models.DateField(auto_now=True)
    status = models.PositiveSmallIntegerField(choices=IP_STATUS)


    def save(self, *args, **kwargs):
        """ Overriden to clear Cache after a new IP is added """
        cache.delete(BLOCKED_IPS_CACHE_KEY)
        super(IPNonGrata, self).save(*args, **kwargs)
