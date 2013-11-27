""" Dump each page of results to it's own hocr html page so we can display it one page at a time. 
Note that the data we're dealing with seems to suffer from this tesseract bug:
https://groups.google.com/forum/#!topic/tesseract-ocr/UiyIMUWMzsU
so we're assuming it's actually latin-1 encoded. 

"""

import unicodedata

from lxml import etree
from lxml.etree import tostring
from StringIO import StringIO

from document_parser import document_parser
from parse_utils import get_words_from_page, get_words_with_lines_from_page, get_annotated_bbox


flexible_parser = etree.XMLParser(encoding='utf-8', recover=True)


file_name = "58-1723645_990_201204"

file_path = "test_hocr/" + file_name + ".html"
parser = document_parser(file_path)

page_num = 0
while True:
    this_page = parser.read_page()
    if not this_page:
        break
    page_num += 1
    print "Processing page %s" % page_num
    outfile = "display/hocr_pages/" + file_name + "p" + str(page_num) + ".html"
    #outh = open(outfile, 'w')
    page_xml = this_page.getvalue()
    page_xml = page_xml.decode('latin-1', 'ignore').encode('utf-8')
    tree = etree.parse(StringIO(page_xml), flexible_parser)
#    tree = etree.parse(StringIO(page_xml))
    tree.write(outfile)
    #outh.write()
    #outh.close()
    