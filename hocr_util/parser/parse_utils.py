""" Assumes word ids are page"""

from lxml import etree, objectify
from lxml.etree import tostring
from StringIO import StringIO

from parse_errors import PageCountError

flexible_parser = etree.XMLParser(encoding='utf-8', recover=True)



# convenience method for naming which coordinates is which in the bbox. I always forget which is which.
def get_annotated_bbox(raw_bbox_string):
    # https://docs.google.com/document/d/1QQnIQtvdAC_8n92-LhwPcjtAUFwBlzE8EWnKAxlgVf0/preview
    # x0 y0 x1 y1
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
    # This is brittle, but seems to work
    return title.lstrip('bbox ')

## There seem to be to variants of the hocr -- one has span class of 'ocr_word' the other users 'ocrx_word'. We're just looking for a class that starts with ocr_word, but I dunno if that's good, of if we'll find other problems in later dox.

# flatten the entire page into just an array of words
def get_words_only(word_tree):
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
        word_array.append({'bbox':get_bbox_from_title(word.attrib['title']), 'text':tostring(word, method="text", encoding='UTF-8'), 'word_num':word.attrib['id'].replace("word_","")})
    return word_array
    

def get_words_from_line(etree, line_id, line_num):
    #print "line id: %s" % line_id
    word_array = []
    xpath_query = "//body/div[@class='ocr_page']/div[@class='ocr_carea']/p[@class='ocr_par']/span[@class='ocr_line' and @id='" + line_id + "']/span[starts-with(@class, 'ocr')]"
    #xpath_query1 = "//body/div[@class='ocr_page']/div[@class='ocr_carea']/p[@class='ocr_par']/span[@class='ocr_line' and @id='" + line_id + "']/span[@class='ocr_word']"
    #xpath_query2 = "//body/div[@class='ocr_page']/div[@class='ocr_carea']/p[@class='ocr_par']/span[@class='ocr_line' and @id='" + line_id + "']/span[@class='ocrx_word']"
    hocr_words = etree.xpath(xpath_query)
    # hocr_words = etree.xpath(xpath_query1)
    #if not hocr_words:
    #    hocr_words = etree.xpath(xpath_query2)
    for word in hocr_words:
        # the text may be contained in this span, but it may also be contained in a child element.
        word_array.append({'bbox':get_bbox_from_title(word.attrib['title']), 'text':tostring(word, method="text", encoding='UTF-8'), 'word_num':word.attrib['id'].replace("word_",""), 'line_num':line_num})
    return word_array

# flatten the page into a two-level hierarchy: lines, which contain words.
def get_lines_with_words(line_tree):
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
    
    
# return just the words from an hocr page
def get_words_from_page(hocr_page):
    tree = etree.parse(StringIO(hocr_page), flexible_parser)
    page_details = get_page_details(tree)
    words = get_words_only(tree)
    return {'attrib': page_details, 'words':words}
    
def get_words_with_lines_from_page(hocr_page):
    tree = etree.parse(StringIO(hocr_page), flexible_parser)
    page_details = get_page_details(tree)
    words = get_lines_with_words(tree)
    return {'attrib': page_details, 'words':words}

