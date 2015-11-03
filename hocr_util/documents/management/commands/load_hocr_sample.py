""" 
Try loading a 1000-document hocr sample into the db. 
Assumes that the 1000-file hocr sample is loaded into the SAMPLE_FILE_DIR

"""
import os, re

from django.core.management.base import BaseCommand, CommandError

from load_utils.load_document import enter_singlepage_document
from datetime import datetime

from hocr_parser.parse_errors import PageCountError


# where the files at?
SAMPLE_FILE_DIR = 'parser/hocr_sample/'
# Because this could take seriously long
FILE_ENTRY_CAP = 1000000

#SAMPLE_FILE_DIR = '/Users/jfenton/github-whitelabel/jsk_project/jsk_management/who-dt_docs/whodt_hocr/'
SAMPLE_FILE_DIR = '/Users/jfenton/github-whitelabel/jsk_project/jsk_management/ca_childcare_docs/page_scans/'
DOCUMENT_COLLECTION_SLUG = 'CA-CHILDCARE'
DOCUMENT_NAME_RE = re.compile("(.+?)\-p(\d+).html")


warning_message = """
No html files were found to enter. You must download the hocr sample and unzip
it, then set that directory as the SAMPLE_FILE_DIR in the body of this command.
The sample files are not included as part of the repo, but are available here:
http://pdf-liberation.s3.amazonaws.com/hocr_sample.zip
"""

class Command(BaseCommand):
    help = "test by loading documents from the SAMPLE_FILE_DIR"
    requires_system_checks = False

    def handle(self, *args, **options):
        

        start = datetime.now()
        files_found = 0
        for d, _, files in os.walk(SAMPLE_FILE_DIR):
            
            for i, this_file in enumerate(files):
                files_found += 1
                file_path = SAMPLE_FILE_DIR + this_file
                # ignore files that aren't .html in case any got mixed in there
                # may want to filter on other criteria here too
                if file_path.find(".html") > 0 and i < FILE_ENTRY_CAP:
                    doc_id = this_file
                    ## we are entering documents that are of the form: %-pn.html
                    ## but use the doc_id without the paginatino
                    result = DOCUMENT_NAME_RE.search(this_file)
                    doc_id = result.group(1)
                    page_number = result.group(2)
                    print "Doc id is: %s file_path is %s page_number = %s" % (doc_id, file_path, page_number)
                        
                    
                    
                    try:
                        enter_singlepage_document(file_path, doc_id, DOCUMENT_COLLECTION_SLUG, page_number, only_enter_new_pages=False)
                        
                    except PageCountError:
                        
                        print "Error entering file number %s from %s - entire document skipped. " % (i, file_path)
                        print traceback.print_exc()
        
        if files_found ==0:
            print warning_message
            
        else:
            end = datetime.now()
            elapsed = end-start
            print "Time elapsed: %s" % (elapsed)