""" Hardcode some test pages--this should be part of the document pipeline etc. 
"""
## cStringIO can't deal w/ unicode, so we're stuck with StringIO
#from cStringIO import StringIO
from StringIO import StringIO

from django.core.management.base import BaseCommand, CommandError
from documents.models import PageWord, Page, Document_Collection

COLLECTION_SLUG = 'WHO-DT'


class Command(BaseCommand):
    help = "set image urls"
    requires_system_checks = False

    def handle(self, *args, **options):
        this_collection = Document_Collection.objects.get(collection_slug=COLLECTION_SLUG)
        unset_pages = Page.objects.filter(doc__document_collection=this_collection)
        
        for (i, this_page) in enumerate(unset_pages):
            
            print "processing page %s with pk=%s" % (i, this_page.pk)
            
            this_page_words_objects = PageWord.objects.filter(page_pk=this_page.pk).order_by('line_num', 'word_num')
            this_page_words = this_page_words_objects.values('text', 'line_num', 'word_num')
            cur_line_num = 1
            
            this_page_string = StringIO()
            this_line_string = StringIO()
            
            for pw in this_page_words:
                #print "running line %s" % (pw['line_num'])
                this_line_num = pw['line_num']
                if this_line_num == cur_line_num:
                    this_line_string.write(' %s' % pw['text'])
                    
                elif this_line_num == cur_line_num + 1:
                    cur_line_num += 1
                    this_page_string.write(this_line_string.getvalue())
                    this_page_string.write("\n")
                    this_line_string = StringIO()
                    this_line_string.write(' %s' % pw['text'])
                    
            this_page.page_text = this_page_string.getvalue()
            this_page.save()



