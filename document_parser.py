""" lazily read an hocr document, returning pages until it's done. Pages are returned as cStringIO objects. Expects strict hocr adherence--</html> must appear on it's own line to end a page... """

from cStringIO import StringIO

class document_parser(object):
    
    def __init__(self, file_path):
        self.file_source = open(file_path, 'r')
        self.pages_read = 0
        self.is_err = False
        
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
            page_to_return.write(this_line)
        self.pages_read += 1
        return page_to_return
        
