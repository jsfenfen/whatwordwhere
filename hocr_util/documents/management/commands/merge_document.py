"""
Merge pages into documents
"""
from django.core.management.base import BaseCommand, CommandError
from documents.models import Document, Page



def merge_by_title(doctitle):
    print "merge by title: %s" % (doctitle)
    

    try:
        # if it already exists do not recreate it
        page_base = Document.objects.get(document_id=doctitle)
    except Document.DoesNotExist:
        first_page.document_id = doctitle
        first_page.save()
    
    for other_doc in other_pages:
        child_pages = Page.objects.filter(doc=other_doc)
        for child_page in child_pages:
            print "Handling page: %s" % (child_page)
            child_page_number = int(child_page.doc.document_id.split("-p")[1])
            child_page.doc=first_page
            child_page.page_number = child_page_number
            child_page.save()
        other_doc.delete()

class Command(BaseCommand):
    help = "merge documents"
    requires_system_checks = False
            
        
    def handle(self, *args, **options):
        
        all_pages = Page.objects.all()
        for page in all_pages:
            
            
        for docpage in documents:
            doctitle = docpage.document_id.split("-p")[0]
            
            merge_by_title(doctitle)