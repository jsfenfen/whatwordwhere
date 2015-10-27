from django.conf.urls import patterns, include, url

from documents import views

urlpatterns = patterns('',
    url(r'^collections/$', 'documents.views.collections', name='collections'),
    url(r'^collection/(?P<slug>[\w\d\-]+)/$', 'documents.views.collection_details', name='collection_details'),
    url(r'^all/$', 'documents.views.show_all', name='all_docs'),
    url(r'^collection/(?P<slug>[\w\d\-]+)/(?P<doc_id>[\w\d\-]+)/$','documents.views.document_page_list',  name='document_page_list'),
    url(r'^collection/(?P<slug>[\w\d\-]+)/(?P<doc_id>[\w\d\-]+)/(?P<page_number>\d+)/$','documents.views.document_page_details',  name='document_page_details'),
    url(r'^geojson/(?P<slug>[\w\d\-]+)/(?P<doc_id>[\w\d\-]+)/p(?P<page_number>\d+).geojson$', 'documents.views.document_page_geojson', name='document_page_geojson'),
)

