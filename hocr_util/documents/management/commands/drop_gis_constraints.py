""" 
Drop GIS constraints that we will be disregarding. Will fail silently.
Assumes that models have default names. 
Would be nice if we could run this from the post_sync signal
But there's a bug in that, apparently.
See: https://code.djangoproject.com/ticket/7561
"""

from django.core.management.base import BaseCommand, CommandError
from django.db import connection

kill_constraints = """
alter table documents_pageword drop constraint "enforce_srid_poly";
alter table documents_pageword drop constraint "enforce_dims_poly";
alter table documents_pageword drop constraint "enforce_geotype_poly";
"""
# We don't really need the last two, but...

class Command(BaseCommand):
    help = "Drop GIS constraints that we will be disregarding. Will fail silently."
    requires_model_validation = False

    def handle(self, *args, **options):
        print "Trying to remove GIS constraints"
        cursor = connection.cursor()
        cursor.execute(kill_constraints)