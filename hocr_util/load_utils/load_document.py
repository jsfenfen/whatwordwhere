import re

from parser.document_parser import document_parser
from parser.parse_utils import get_words_from_page
from documents.models import Document, Page, PageWord
from load_utils.load_page import enter_words

from django.contrib.gis.geos import GEOSGeometry

parser = None
bbox_re = re.compile(r'bbox\s+(.+)')

def enter_page(doc, page, page_number):
    print "processing page %s" % page_number
    page_attributes =  page['attrib']
    title = page_attributes['title']
    r = bbox_re.search(title)
    
    bbox_raw = r.group(1)
    coords = bbox_raw.split()
    p = {
        'xmin':coords[0], 
        'ymin':coords[1], 
        'xmax':coords[2], 
        'ymax':coords[3]
    }
    
    
    poly_string = """POLYGON((%s %s, %s %s,%s %s,%s %s,%s %s))""" % (
        p['xmin'], p['ymin'], p['xmin'], p['ymax'], p['xmax'], 
        p['ymax'], p['xmax'], p['ymin'],p['xmin'], p['ymin'] 
    )
    
    poly = GEOSGeometry(poly_string)
    wkb = poly.hex
    this_page, created = Page.objects.get_or_create(
        doc=doc, 
        page_number=page_number, 
        defaults={'page_dimensions':poly}
    )
    
    page_pk = this_page.pk
    enter_words(page_pk, page['words'])
    
# Ignore whatever internal pagination there is, and count pages ourselves. 
# This may cause trouble later, I dunno.
def enter_document(file_path, document_id):
    parser = document_parser(file_path, encoding='latin-1')
    this_doc, created = Document.objects.get_or_create(document_id=document_id)
    # todo: populate ein, form, year, month from id
    page_count=0
    for this_page in parser:
        page_count += 1
        
        # READ THE PAGE AS A BUNCH OF WORDS ONLY
        page = get_words_from_page(this_page.getvalue())
        enter_page(this_doc, page, page_count)



    
    