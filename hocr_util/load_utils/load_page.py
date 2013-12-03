import csv

from cStringIO import StringIO

from django.contrib.gis.geos import GEOSGeometry
from django.db import connection

from parser.document_parser import document_parser
from parser.parse_utils import get_words_from_page
from documents.models import Document, Page, PageWord
from geo_utils.word_shapes import get_word_shapes


cursor = connection.cursor()
fields = ['page_pk', 'word', 'bbox']


def enter_words(page_pk, word_array):
    transactions_to_commit = StringIO()
    writer = csv.DictWriter(transactions_to_commit, fields, restval="", extrasaction='ignore', lineterminator='\n', delimiter=";", quoting=csv.QUOTE_ALL, quotechar='"', escapechar='\\')
    
    word_array = get_word_shapes(word_array)
    
    for word in word_array:
        text = word['text']
        wkb = word['poly'].hex
        #print "data: %s %s %s" % (page_pk, text, wkb)
        writer.writerow({'page_pk':page_pk, 'word':text, 'bbox': wkb})
    
    length = transactions_to_commit.tell()
    transactions_to_commit.seek(0)
    sql = "COPY documents_pageword (page_pk, word, bbox) FROM STDIN delimiter ';' escape '\\' quote '\"' CSV "
    cursor.copy_expert(sql, transactions_to_commit, size=length)    
        