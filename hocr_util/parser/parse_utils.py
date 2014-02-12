""" Utility functions to help parse hocr data. Django-independent. """

from lxml import etree, objectify
from lxml.etree import tostring
from StringIO import StringIO

from parse_errors import PageCountError

# The source data can be amazingly awful. Try to recover as much as possible. 
# We could do a better job of this, maybe, by assuming only certain input characters were legal.
# Crazy characters are often not used in tax returns, for instance. 

flexible_parser = etree.XMLParser(encoding='utf-8', recover=True)

def simple_clean(word):
    """
    Placeholder for text processing that needs to take place at the very start of the process.
        Stuff here gets applied before it's returned in any form. 
    """
    # it seems like words often have leading / trailing spaces
    return word.strip()
    

def get_annotated_bbox(raw_bbox_string):
    """ Convenience method for naming which coordinates is which in the bbox. I always forget which is which. 
        See: https://docs.google.com/document/d/1QQnIQtvdAC_8n92-LhwPcjtAUFwBlzE8EWnKAxlgVf0/preview
        x0 y0 x1 y1
    """
    coords = raw_bbox_string.split()
    return {'xmin':coords[0], 'ymin':coords[1], 'xmax':coords[2], 'ymax':coords[3]}
    
def get_page_details(page_tree):
    ocr_page = page_tree.xpath("//body/div[@class='ocr_page']")
    # Raise an error if we have more than one page -- this happens occasionally, not sure why yet. 
    num_pages = len(ocr_page)
    if num_pages != 1:
        print "%s" % (tostring(page_tree))
        raise PageCountError ("Pages count mismatch: %s pages found" % (num_pages))
        
    return ocr_page[0].attrib
    
def get_bbox_from_title(title):
    ## This is brittle, but seems to work
    ## There seem to be to variants of the hocr -- one has span class of 'ocr_word' the other users 'ocrx_word'. We're just looking for a class that starts with ocr_word, but I dunno if that's good, or if we'll find other problems in later dox.
    return title.lstrip('bbox ')


def get_words_only(word_tree):
    """ Return a python dict by flattening the entire page into just an array of words.
    This discards line number information, and is really just here as a historical thing.
    """
    
    word_array = []
    xpath_query = "//body/div[@class='ocr_page']/div[@class='ocr_carea']/p[@class='ocr_par']/span[@class='ocr_line' and @id='" + line_id + "']/span[starts-with(@class, 'ocr')]"
    #xpath_query1 = "//body/div[@class='ocr_page']/div[@class='ocr_carea']/p[@class='ocr_par']/span[@class='ocr_line' and @id='" + line_id + "']/span[@class='ocr_word']"
    #xpath_query2 = "//body/div[@class='ocr_page']/div[@class='ocr_carea']/p[@class='ocr_par']/span[@class='ocr_line' and @id='" + line_id + "']/span[@class='ocrx_word']"
    hocr_words = etree.xpath(xpath_query)
    #if not hocr_words:
    #    hocr_words = etree.xpath(xpath_query2)
    for word in hocr_words:
        #print word.attrib
        # the text may be contained in this span, but it may also be contained in a child element.
        word_array.append({'bbox':get_bbox_from_title(word.attrib['title']), 'text':simple_clean(tostring(word, method="text", encoding='UTF-8')), 'word_num':word.attrib['id'].replace("word_","")})
    return word_array
    

def get_words_from_line(etree, line_id, line_num):
    """ Return a python dict by flattening the entire page into just an array of words.
    This discards line number information, and is really just here as a historical thing.
    """
    #print "line id: %s" % line_id
    word_array = []
    xpath_query = "//body/div[@class='ocr_page']/div[@class='ocr_carea']/p[@class='ocr_par']/span[@class='ocr_line' and @id='" + line_id + "']/span[starts-with(@class, 'ocr')]"
    
    ## Have noodled with this some--these used to work. It's not clear that xpath really can handle the range of hocr formats that will be thrown at us, but it works when formats are fairly uniform.
    #xpath_query1 = "//body/div[@class='ocr_page']/div[@class='ocr_carea']/p[@class='ocr_par']/span[@class='ocr_line' and @id='" + line_id + "']/span[@class='ocr_word']"
    #xpath_query2 = "//body/div[@class='ocr_page']/div[@class='ocr_carea']/p[@class='ocr_par']/span[@class='ocr_line' and @id='" + line_id + "']/span[@class='ocrx_word']"
    hocr_words = etree.xpath(xpath_query)
    # hocr_words = etree.xpath(xpath_query1)
    #if not hocr_words:
    #    hocr_words = etree.xpath(xpath_query2)
    for word in hocr_words:
        # the text may be contained in this span, but it may also be contained in a child element.
        word_array.append({'bbox':get_bbox_from_title(word.attrib['title']), 'text':simple_clean(tostring(word, method="text", encoding='UTF-8')), 'word_num':word.attrib['id'].replace("word_",""), 'line_num':line_num})
    return word_array

def get_lines_with_words(line_tree):
    """ Flatten the page into a two-level hierarchy: lines, which contain words. """

    #print tostring(line_tree)
    word_array = []
    hocr_lines = line_tree.xpath("//body/div[@class='ocr_page']/div[@class='ocr_carea']/p[@class='ocr_par']/span[@class='ocr_line']")
    for line in hocr_lines:
        #print "line attribs is %s" % (line.attrib)
        this_line = {}
        this_line['attrib'] = line.attrib
        line_id = line.attrib['id']
        line_num = line_id.replace("line_","")
        this_line_words = get_words_from_line(line, line_id, line_num)
        word_array = word_array + this_line_words
    return word_array
    
    
def get_words_from_page(hocr_page):
    """ Return just the words from an hocr page. """
    tree = etree.parse(StringIO(hocr_page), flexible_parser)
    page_details = get_page_details(tree)
    words = get_words_only(tree)
    return {'attrib': page_details, 'words':words}
    
def get_words_with_lines_from_page(hocr_page):
    """ Return words with lines from an hocr page. """
    tree = etree.parse(StringIO(hocr_page), flexible_parser)
    page_details = get_page_details(tree)
    words = get_lines_with_words(tree)
    return {'attrib': page_details, 'words':words}

