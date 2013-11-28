import csv

from cStringIO import StringIO

from django.contrib.gis.geos import GEOSGeometry
from django.db import connection

from parser.document_parser import document_parser
from parser.parse_utils import get_words_from_page
from documents.models import Document, Page, PageWord

cursor = connection.cursor()
fields = ['page_pk', 'word', 'bbox']


def enter_words(page_pk, word_array):
    transactions_to_commit = StringIO()
    writer = csv.DictWriter(transactions_to_commit, fields, restval="", extrasaction='ignore', lineterminator='\n', delimiter=";", quoting=csv.QUOTE_ALL, quotechar='"', escapechar='\\')
    
    
    
    for word in word_array:
        text = word['text']
        bbox_raw = word['bbox']
        coords = bbox_raw.split()
        p = {'xmin':coords[0], 'ymin':coords[1], 'xmax':coords[2], 'ymax':coords[3]}
        poly_string = """POLYGON((%s %s, %s %s,%s %s,%s %s,%s %s))""" % (p['xmin'], p['ymin'], p['xmin'], p['ymax'], p['xmax'], p['ymax'], p['xmax'], p['ymin'],p['xmin'], p['ymin'] )
        poly = GEOSGeometry(poly_string)
        wkb = poly.hex
        #print "data: %s %s %s" % (page_pk, text, wkb)
        writer.writerow({'page_pk':page_pk, 'word':text, 'bbox': wkb})
    
    
    
    length = transactions_to_commit.tell()
    transactions_to_commit.seek(0)
    sql = "COPY documents_pageword (page_pk, word, bbox) FROM STDIN delimiter ';' escape '\\' quote '\"' CSV "
    cursor.copy_expert(sql, transactions_to_commit, size=length)    
        