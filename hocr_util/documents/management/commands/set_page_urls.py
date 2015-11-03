""" Harcode some test pages--this should be part of the document pipeline etc. 
"""

from django.core.management.base import BaseCommand, CommandError
from documents.models import Page, Document

class Command(BaseCommand):
    help = "set image urls"
    requires_system_checks = False

    def handle(self, *args, **options):
        unset_pages = Page.objects.filter(doc__document_collection__collection_slug=='WHO-DT')
        for p in unset_pages:
            image_url = "http://jacobfenton.s3.amazonaws.com/hocr/collections/WHO-DT/" + p.doc.document_id + "-p" + str(p.page_number) + ".png"
            thumbnail_url = "http://jacobfenton.s3.amazonaws.com/hocr/collections/WHO-DT/" + p.doc.document_id + "-thumb-p" + str(p.page_number) + ".png"
            p.image = image_url
            p.thumbnail = thumbnail_url
            p.save() 


