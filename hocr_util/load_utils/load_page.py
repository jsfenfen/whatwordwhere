"""
Load a page of hocr data to a postgis database assuming django's template naming conventions, 
in other words, assume that it was created by django.
This is sorta a hack that uses csv to write to a cstring which is then the source of a bulk insert to postgis. 
"""

import csv

from cStringIO import StringIO

from django.contrib.gis.geos import GEOSGeometry
from django.db import connection

from hocr_parser.document_parser import document_parser
from hocr_parser.parse_utils import get_words_from_page
from documents.models import Document_Collection, Document, Page, PageWord
from geo_utils.word_shapes import get_word_shapes


cursor = connection.cursor()
fields_without_lines = ['page_pk', 'text', 'bbox', 'poly', 'word_num']
fields = ['page_pk', 'text', 'bbox', 'poly', 'word_num', 'line_num']


ESCAPE_CHAR = '^'
DOUBLE_ESCAPE_CHAR = '^^'
QUOTE_CHAR = '`'

def word_clean(raw_word):
    # csv's dictwriter seems to not escape the escape character in quoted strings (or, at least, I've somehow told it not to). We can either manually escape it, or just remove it. 
    # manually escaping seems to work
    raw_word = raw_word.replace(ESCAPE_CHAR,DOUBLE_ESCAPE_CHAR)
    
    # If we don't care about the escape char, we can just chuck it. 
    #raw_word = raw_word.replace(ESCAPE_CHAR,"")
    return raw_word

def enter_words_only(page_pk, word_array):
    transactions_to_commit = StringIO()
    writer = csv.DictWriter(transactions_to_commit, fields_without_lines, restval="", extrasaction='ignore', lineterminator='\n', delimiter=";", quoting=csv.QUOTE_ALL, quotechar=QUOTE_CHAR, escapechar=ESCAPE_CHAR)
    
    word_array = get_word_shapes(word_array)
    
    for word in word_array:
        wkb = word['poly'].hex
        word_fixed = word_clean(word['text'])
        #print "data: %s %s %s" % (page_pk, text, wkb)
        writer.writerow({'page_pk':page_pk, 'text':word_fixed, 'bbox':word['bbox'], 'poly': wkb, 'word_num':word['word_num'] })
    
    length = transactions_to_commit.tell()
    transactions_to_commit.seek(0)
    sql = "COPY documents_pageword (page_pk, text, bbox, poly, word_num) FROM STDIN delimiter ';' escape '%s' quote '%s' CSV " % (ESCAPE_CHAR, QUOTE_CHAR)
    cursor.copy_expert(sql, transactions_to_commit, size=length)    
        

def enter_words(page_pk, word_array):
    transactions_to_commit = StringIO()
    writer = csv.DictWriter(transactions_to_commit, fields, restval="", extrasaction='ignore', lineterminator='\n', delimiter=";", quoting=csv.QUOTE_ALL, quotechar=QUOTE_CHAR, escapechar=ESCAPE_CHAR)

    word_array = get_word_shapes(word_array)
    #print "Entering words, with word length %s" % (len(word_array))
    

    for word in word_array:
        wkb = word['poly'].hex
        #print "data: %s %s %s" % (page_pk, word['text'], wkb)
        word_fixed = word_clean(word['text'])
        writer.writerow({'page_pk':page_pk, 'text':word_fixed, 'bbox':word['bbox'], 'poly': wkb, 'word_num':word['word_num'], 'line_num':word['line_num']})

    length = transactions_to_commit.tell()
    
    ## debug raw sql output for quoting etc issues (ugh) with:
    print transactions_to_commit.getvalue()
    
    transactions_to_commit.seek(0)
    sql = "COPY documents_pageword (page_pk, text, bbox, poly, word_num, line_num) FROM STDIN delimiter ';' escape '%s' quote '%s' CSV " % (ESCAPE_CHAR, QUOTE_CHAR)
    cursor.copy_expert(sql, transactions_to_commit, size=length)