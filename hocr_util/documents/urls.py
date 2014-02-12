from django.conf.urls import patterns, include, url

from documents import views

urlpatterns = patterns('',
    url(r'^all/$', 'documents.views.show_all', name='all_docs'),
    url(r'^document/(?P<doc_id>[\w\d\-]+)/$','documents.views.document_pages',  name='document_pages'),
    url(r'^geojson/(?P<doc_id>[\w\d\-]+)/p(?P<page_number>\d+).geojson$', 'documents.views.document_page_geojson', name='document_page_geojson'),
)

