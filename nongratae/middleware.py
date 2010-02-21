# -*- coding: utf-8 -*-

"""
Middleware class that spots requests and analizes them for suspicies behavior
after a number of hits by the suspicios IP are detected the IP is blocked

Blocked IPs get a response with the motive of their blocking
"""

from django.core.cache import cache
from django.conf import settings

from nongratae.constants import BLOCKED_IPS_CACHE_TIMEOUT, BLOCKED_IPS_CACHE_KEY
from nongratae.models import BlockedIP

SITE_ID = settings.SITE_ID
BLOCKED_IPS_CACHE_KEY = BLOCKED_IPS_CACHE_KEY % SITE_ID

def get_blocked_ips():
    
    blocked_ips = cache.get(BLOCKED_IPS_CACHE_KEY)
    if blocked_ips is None:
        blocked_ips = {}

        for bi in  BlockedIP.objects.fitler(status=BlockedIP.BLOCKED,
            site_id=SITE_ID):

            blocked_ips[bi.ip] = bi.motive

        cache.set(BLOCKED_IPS_CACHE_KEY, blocked_ips, BLOCKED_IPS_CACHE_TIMEOUT)

    return blocked_ips
    

class IpNonGratae(object):

    def process_request(self, request):
        """
        If the IP is blocked return the motive as a response

        If the IP is not blocked, track its behavior to detect 
        malicious IPs
        """

        ip = request.META['REMOTE_ADDR']
        blocked_ips = get_blocked_ips()

        # ip is blocked
        if ip in blocked_ips:
            return HttpResponse(blocked_ips[ip])


        
