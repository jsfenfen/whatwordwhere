""" 
Test management command to load a single document into the db, including GEOS stuff. 
"""

from django.core.management.base import BaseCommand, CommandError
from load_utils.load_document import enter_document
from datetime import datetime

# SAMPLE_FILE_DIR = '/Users/jfenton/github-whitelabel/whatwordwhere/whatwordwhere/display/page_scans/'
# DOCUMENT_COLLECTION_SLUG = 'ca-childcare'
SAMPLE_FILE_DIR = '/Users/jfenton/github-whitelabel/jsk_project/jsk_management/who-dt_docs/whodt_hocr/'
DOCUMENT_COLLECTION_SLUG = 'WHO-DT'

class Command(BaseCommand):
    help = "test by loading a document"
    requires_system_checks = False

    def handle(self, *args, **options):
        # sample file included with repo, hopefully
        #doc_id = "1088501-adventuretime-alta-p1"
        doc_id = "14400741771771-p2"
        this_file = SAMPLE_FILE_DIR  + doc_id + ".html"
        # 1088501-adventuretime-alta-p1.png
        start = datetime.now()
        enter_document(this_file, doc_id, DOCUMENT_COLLECTION_SLUG, only_enter_new_pages=False)
        end = datetime.now()
        elapsed = end-start
        print "Time elapsed: %s" % (elapsed)