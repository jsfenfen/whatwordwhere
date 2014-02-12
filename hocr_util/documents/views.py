from django.shortcuts import get_object_or_404, render_to_response, render
from django.http import HttpResponse

from geo_utils.geojson_utils import get_feature_collection

from documents.models import Document, Page, PageWord

def show_all(request):
    # just use 100 as a sample here. 
    docs = Document.objects.all()[:100]
    return render_to_response('documents/doclist.html', 
        {'docs':docs}
    )

def document_pages(request, doc_id):
    # all pages of a document
    doc = get_object_or_404(Document, document_id=doc_id)
    pages = Page.objects.filter(doc__document_id=doc_id).order_by('page_number')
    
    return render_to_response('documents/pagelist.html', {
        'pages':pages,
        'doc':doc,
    })
        
def document_page_geojson(request, doc_id, page_number):
    
    this_page = get_object_or_404(Page, doc__document_id=doc_id, page_number=page_number)
    this_page_words = PageWord.objects.filter(page_pk=this_page.pk).values('text','bbox', 'line_num')
    print this_page_words[0]
    page = {}
    page['words'] = this_page_words        
    output = get_feature_collection(page)
    # todo: add the page bounding box. 
    
    return HttpResponse(output, content_type="application/json")

