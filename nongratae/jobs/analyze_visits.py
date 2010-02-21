# -*- coding: utf-8 -*-

from django_extensions.management.jobs import BaseJob

from nongratae.models import Visit, IPNonGrata

class Job(BaseJob):

    help = "Runs analyze filters over visits made and blocks IPs if needed"

    def execute(self):
        all_visits = Visit.objects.all()
