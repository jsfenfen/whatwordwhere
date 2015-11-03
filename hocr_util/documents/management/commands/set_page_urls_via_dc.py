""" Set the image urls according to DocumentCloud conventions, assuming the whole slug thing is the document_slug
"""
import re

from dc_utils.url_helpers import parse_dc_slug, get_normal_image_url, get_thumbnail_image_url

from django.core.management.base import BaseCommand, CommandError
from documents.models import Page, Document, Document_Collection

document_cloud_slugs_re = re.compile('(\d+)-(.+)')
COLLECTION_SLUG = 'CA-CHILDCARE'

class Command(BaseCommand):
    help = "set image urls"
    requires_system_checks = False

    def handle(self, *args, **options):
        this_collection = Document_Collection.objects.get(collection_slug=COLLECTION_SLUG)
        unset_pages = Page.objects.filter(doc__document_collection=this_collection)
        for p in unset_pages:
            
            result =  parse_dc_slug(p.doc.document_slug)
            print result
            p.image = get_normal_image_url(result['id'], result['slug'], p.page_number)
            p.thumbnail = get_thumbnail_image_url(result['id'], result['slug'], p.page_number)
            p.save() 


