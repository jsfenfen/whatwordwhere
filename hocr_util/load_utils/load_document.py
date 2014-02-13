import re, traceback

from hocr_parser.document_parser import document_parser
from hocr_parser.parse_utils import get_words_from_page, get_words_with_lines_from_page
from documents.models import Document, Page, PageWord
from load_utils.load_page import enter_words
from geo_utils.word_shapes import get_poly_string_from_bbox

from django.contrib.gis.geos import GEOSGeometry


parser = None
bbox_re = re.compile(r'bbox\s+(.+)\;*')
ppageno_re = re.compile(r'; ppageno \d+')

# ignore the line numbers. This is essentially deprecated, but left here in case it becomes useful again. 
def enter_page_words_only(doc, page, page_number):
    print "processing page %s" % page_number
    page_attributes =  page['attrib']
    title = page_attributes['title']
    r = bbox_re.search(title)
    
    bbox_raw = r.group(1)
    poly_string = get_poly_string_from_bbox(bbox_raw)
    poly = GEOSGeometry(poly_string)
    wkb = poly.hex
    this_page, created = Page.objects.get_or_create(
        doc=doc, 
        page_number=page_number, 
        defaults={'page_dimensions':poly}
    )
    
    page_pk = this_page.pk
    # READ THE PAGE AS A BUNCH OF WORDS ONLY
    enter_words_only(page_pk, page['words'])
    
def enter_page(doc, page, page_number):
    #print "processing page %s" % page_number
    page_attributes =  page['attrib']
    title = page_attributes['title']
    #semicolon_position = title.find(';')
    #if semicolon_position > 0:
    #    title = title[:semicolon_position]
    #print "title is '%s'" % title
    #r = bbox_re.search(title)

    #bbox_raw = r.group(1)
    bbox_raw = title.split(';')[1]
    bbox_raw = bbox_raw.replace("bbox ", "")
    poly_string = get_poly_string_from_bbox(bbox_raw)
    #print "bbox is %s, poly_string is: %s" % (bbox_raw, poly_string)
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
        
        # READ THE PAGE AS A HIERARCHY OF LINES AND WORDS. ONLY WORDS ARE GIVEN BOUNDING BOXES HERE THOUGH
        # THE HOCR SPEC GIVES LINES BOUNDING BOXES, SO THEY COULD BE ADDED, IT'S JUST NOT CLEAR IF THAT WOULD HELP
        # I ASSUME THE LINE IS JUST THE CONVEX HULL OF THE WORDS, BUT DON'T KNOW THIS FOR SURE. 
        
        page = get_words_with_lines_from_page(this_page.getvalue())
        enter_page(this_doc, page, page_count)






    
    