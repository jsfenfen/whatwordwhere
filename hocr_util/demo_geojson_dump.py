""" A django-independent test that reads a document and returns geojson files for each page. """

from hocr_parser.document_parser import document_parser
from hocr_parser.parse_utils import get_words_with_lines_from_page
from geo_utils.geojson_utils import get_feature_collection

# A test file
hocr_file = "./hocr_parser/test_hocr/58-1723645_990_201204.html"

# create a parser for this doc
hocr_parser = document_parser(hocr_file, encoding='latin-1')

for this_page in hocr_parser:
    
    # retrieve a representation of the pages that include line numbers and word numbers
    page = get_words_with_lines_from_page(this_page.getvalue())
    
    print "Processing page %s -- now dumping geojson to stdout\n\n" % (page['attrib'])
    # Get geojson that assigns id by word order and preserves line numbers as an attribute
    print get_feature_collection(page)
    print "\n\n\n"