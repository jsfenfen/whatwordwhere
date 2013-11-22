from document_parser import document_parser
from parse_utils import get_words_from_page, get_words_with_lines_from_page, get_annotated_bbox


file = "test_hocr/31-1640316_990_201206.html"

a = document_parser(file)



while True:
    this_page = a.read_page()
    if not this_page:
        break
    
    
    # READ THE PAGE AS A BUNCH OF WORDS ONLY
    
    
    page = get_words_from_page(this_page.getvalue())
    # pages have two attributes: 'attrib' and 'words'
    page_attributes =  page['attrib']
    first_word =  page['words'][0]
    # words have two attributes: 'text' and 'bbox'
    annotated_bbox = get_annotated_bbox(first_word['bbox'])
    print "Processing page %s" % (page_attributes)
    print "Got first word '%s' with bounding_box %s" % (first_word['text'],  annotated_bbox)
    print "\n\n"
    
    
    # READ THE PAGE AS A HIERARCHY OF WORDS CONTAINED IN LINES
    
    page = get_words_with_lines_from_page(this_page.getvalue())
    ## pages have two attributes: 'attrib' and 'lines'
    print page['attrib']
    for line in page['lines']:
        ## lines have two attributes: 'attrib' and 'words'
        print "got line: %s with %s word(s)" % (line['attrib'], len(line['words']))
        print line['words']
        print "\n\n"
