""" 
Try loading a 1000-document hocr sample into the db. 
    assumes that the 1000-file hocr sample is loaded into the SAMPLE_FILE_DIR
"""
import os 

from django.core.management.base import BaseCommand, CommandError

from load_utils.load_document import enter_document
from datetime import datetime

from parser.parse_errors import PageCountError


# where the files at?
SAMPLE_FILE_DIR = 'parser/hocr_sample/'
# Because this could take seriously long
FILE_ENTRY_CAP = 1000

class Command(BaseCommand):
    help = "test by loading a document"
    requires_model_validation = False

    def handle(self, *args, **options):
        
        # just try one that's weird.
        if False:
            file_path = "parser/hocr_sample/02-0575282_990EZ_201212.html"
            doc_id = "02-0575282_990EZ_201212"
            enter_document(file_path, doc_id)
            assert False

        start = datetime.now()
        
        for d, _, files in os.walk(SAMPLE_FILE_DIR):
            for i, this_file in enumerate(files):
                file_path = SAMPLE_FILE_DIR + this_file
                # ignore files that aren't .html in case any got mixed in there
                # may want to filter on other criteria here too
                if file_path.find(".html") > 0 and i < FILE_ENTRY_CAP:
                    doc_id = this_file.replace(".html", "")
                    print "Entering file number %s data from: %s" % (i, file_path)
                    
                    try:
                        enter_document(file_path, doc_id)
                        
                    except PageCountError:
                        
                        print "Error entering file number %s from %s - entire document skipped. " % (i, file_path)
                        print traceback.print_exc()
        
        end = datetime.now()
        elapsed = end-start
        print "Time elapsed: %s" % (elapsed)