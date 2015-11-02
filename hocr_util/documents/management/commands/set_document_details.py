""" Set document summary, thumbnail image, number of pages from page details. 
"""

from django.core.management.base import BaseCommand, CommandError
from documents.models import Document, Page

class Command(BaseCommand):
    help = "set image urls"
    requires_system_checks = False

    def handle(self, *args, **options):
        # maybe take the document collection slug as a command line argument?
        unset_documents = Document.objects.filter(document_collection__collection_slug="WHO-DT")
        
        for (i, this_doc) in enumerate(unset_documents):
            
            print "processing doc #%s" % (i)
            pages = Page.objects.filter(doc=this_doc).order_by('page_number')
            page_count = pages.count()
            print "first page has page number %s and page_count %s" % (pages[0].page_number, page_count)
            
            this_doc.document_summary = pages[0].page_text[:200]
            this_doc.thumbnail = pages[0].thumbnail
            this_doc.page_count = page_count
            
            this_doc.save()

