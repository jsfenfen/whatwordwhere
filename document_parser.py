""" lazily read an hocr document, returning pages until it's done. Pages are returned as cStringIO objects. Expects strict hocr adherence--</html> must appear on it's own line to end a page... 

Also, note that some hocr that's supposed to be utf-8 is actually latin-1. 
https://groups.google.com/forum/#!topic/tesseract-ocr/UiyIMUWMzsU

Pass in the encoding explicitly if it's different.

"""

from cStringIO import StringIO

class document_parser(object):
    
    def __init__(self, file_path, encoding='utf-8'):
        self.file_source = open(file_path, 'r')
        self.pages_read = 0
        self.is_err = False
        self.encoding = encoding
        
    def read_page(self):
        page_to_return = StringIO()
        end_of_page_found=False
        
        while not end_of_page_found:
            try:
                this_line = self.file_source.next()
            except Exception:
                self.is_err = True
                return None
                
            if this_line.startswith("</html>") :
                end_of_page_found = True
            
            if self.encoding != 'utf-8':
                this_line = this_line.decode(self.encoding).encode('utf-8')
            page_to_return.write(this_line)
        self.pages_read += 1
        return page_to_return
        
