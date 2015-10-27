from django.shortcuts import get_object_or_404, render_to_response, render
from django.http import HttpResponse

from geo_utils.geojson_utils import get_feature_collection

from documents.models import Document_Collection, Document, Page, PageWord
import geojson

def show_all(request):
    # just use 100 as a sample here. 
    docs = Document.objects.all()[:100]
    return render_to_response('documents/doclist.html', 
        {'docs':docs,
        'header':"All Documents [truncated at 100]",}
    )

def collections(request):
    collections = Document_Collection.objects.all()
    return render_to_response('documents/collectionlist.html', 
        {'collections':collections}
    )

def collection_details(request, slug):
    coll = get_object_or_404(Document_Collection, collection_slug=slug)
    docs = Document.objects.filter(document_collection=coll)[:100]


    return render_to_response('documents/doclist.html', 
    {'docs':docs,
     'header':slug,}
    )
    
def document_page_list(request, slug, doc_id):
    # all pages of a document
    doc = get_object_or_404(Document, document_id=doc_id, document_collection__collection_slug=slug)
    pages = Page.objects.filter(doc=doc).order_by('page_number')
    
    return render_to_response('documents/pagelist.html', {
        'pages':pages,
        'doc':doc,
    })

def document_page_details(request, slug, doc_id, page_number):
    # all pages of a document
    doc = get_object_or_404(Document, document_id=doc_id, document_collection__collection_slug=slug)
    page = get_object_or_404(Page, doc=doc, page_number=page_number)

    return render_to_response('documents/page.html', {
        'page':page,
        'doc':doc,
    })

        
def document_page_geojson(request, slug, doc_id, page_number):
    this_document = get_object_or_404(Document, document_id=doc_id, document_collection__collection_slug=slug)
    this_page = get_object_or_404(Page, doc__document_id=doc_id, page_number=page_number)
    this_page_words = PageWord.objects.filter(page_pk=this_page.pk).values('text','bbox', 'line_num')
    page = {}
    page['words'] = this_page_words        
    featurecollection = get_feature_collection(page['words'])
    
    ## Add additional attributes needed. This may or may not break the geojsonspec. 
    featurecollection['bbox'] = 'blah'
    featurecollection['background_image'] = 'blahblah'
    
    output = geojson.dumps(featurecollection)
    # todo: add the page bounding box. 
    return HttpResponse(output, content_type="application/json")

