# -*- coding: utf-8 -*-

"""
Middleware class that spots requests and analizes them for suspicies behavior
after a number of hits by the suspicios IP are detected the IP is blocked

Blocked IPs get a response with the motive of their blocking
"""

from django.core.cache import cache
from django.conf import settings

from nongratae.constants import BLOCKED_IPS_CACHE_TIMEOUT, BLOCKED_IPS_CACHE_KEY
from nongratae.models import IPNonGrata, Visit

SITE_ID = settings.SITE_ID
BLOCKED_IPS_CACHE_KEY = BLOCKED_IPS_CACHE_KEY % SITE_ID

FLUSH_VISITS = 3

def get_blocked_ips():
    
    blocked_ips = cache.get(BLOCKED_IPS_CACHE_KEY)
    if blocked_ips is None:
        blocked_ips = {}

        for bi in  IPNonGrata.objects.filter(status=IPNonGrata.BLOCKED,
            site__id=SITE_ID):

            blocked_ips[bi.ip] = bi.motive

        cache.set(BLOCKED_IPS_CACHE_KEY, blocked_ips, BLOCKED_IPS_CACHE_TIMEOUT)

    return blocked_ips
    

class IpNonGrataeMiddleware(object):

    ip_list = [] # It is a good thing this isn't thread safe

    def process_request(self, request):
        """
        If the IP is blocked return the motive as a response

        If the IP is not blocked, track its behavior to detect 
        malicious IPs
        """

        visit = Visit()
        visit.build_from_request(request)
        blocked_ips = get_blocked_ips()

        # ip is blocked
        if visit.ip in blocked_ips:
            return HttpResponse(blocked_ips[ip])
        
        # Ip not blocked, then add it to the queue
        self.ip_list.append(visit) 

        # If reached flush limit, persist them for further analysis via a cron job
        if len(self.ip_list) == FLUSH_VISITS:
            print 'flushing...'
            while self.ip_list:
                visit = self.ip_list.pop()
                visit.save()



