"""
Test management command to dump some geojson files. 
The geojson dumping is django independent, though obviously
running this as a management commands requires it.
"""

import os

from django.core.management.base import BaseCommand, CommandError

from parser.document_parser import document_parser
from parser.parse_utils import get_words_with_lines_from_page
from geo_utils.word_shapes import get_word_shapes
from geo_utils.geojson_utils import get_feature_collection

# where the files at?
SAMPLE_FILE_DIR = 'parser/hocr_sample/'


class Command(BaseCommand):
    help = "test by loading a document"
    requires_model_validation = False

    def handle(self, *args, **options):        
        for d, _, files in os.walk(SAMPLE_FILE_DIR):
            for i, this_file in enumerate(files):
                file_path = SAMPLE_FILE_DIR + this_file
                # ignore files that aren't .html in case any got mixed in there
                # may want to filter on other criteria here too
                if file_path.find(".html") > 0:
                    print "Handling %s" % (file_path)
        
                    parser = document_parser(file_path, encoding='latin-1')
                    first_page = parser.next_document()
                    page = get_words_with_lines_from_page(first_page.getvalue())
                    fc = get_feature_collection(page)
                    print fc
        