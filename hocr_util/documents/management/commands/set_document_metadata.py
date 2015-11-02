""" Set document metadata field from csv file. Eventually this needs a real process. 
"""
import csv 

from django.core.management.base import BaseCommand, CommandError
from documents.models import Document, Page

INPUT_CSV = '/Users/jfenton/github-whitelabel/jsk_project/jsk_management/who-dt_docs/WHO-DT.csv'

class Command(BaseCommand):
    help = "set image urls"
    requires_system_checks = False

    def handle(self, *args, **options):
        
        infile = open(INPUT_CSV,'rb')
        
        # maybe take the document collection slug as a command line argument?
        unset_documents = Document.objects.filter(document_collection__collection_slug="WHO-DT")
        filedata = next(infile)        
        reader = csv.DictReader(infile)
        for row in reader:
            if not row['file_url']:
                continue
            document_id = row['fcc_id']
            searchable_url = row['file_url']
            searchable_url = searchable_url.replace("%28", "(")
            searchable_url = searchable_url.replace("%29", ")")
            upload_time = row['upload_time']
            this_doc_metadata = {'upload_time':upload_time, 'searchable_url':searchable_url}
            print "Got id=%s, data %s" % (document_id, this_doc_metadata)
            
            this_doc = Document.objects.get(document_id=document_id)
            this_doc.metadata = this_doc_metadata
            this_doc.save()
