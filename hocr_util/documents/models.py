""" Django models for document, pages, and words on pages (page_words).
    Assumes the db uses utf-8 encoding
"""

from django.contrib.gis.db import models
from django_hstore import hstore

# We may want to convert url fields to image fields, but b/c the process
# is pretty uncoupled with processing the images, text seems fine now

class Document_Collection(models.Model):
    collection_name = models.TextField()
    collection_slug = models.SlugField()
    collection_description = models.TextField(blank=True, null=True)
    #collection_document_count = models.IntegerField(null=True)
    #collection_page_count = models.IntegerField(null=True)
    ## eventually need ownership, permissions. 
    
    def get_absolute_url(self):
        return "/documents/collection/%s/" % (self.collection_slug)



class Document(models.Model):
    document_id = models.CharField(max_length=63, unique=True, primary_key=True)
    document_slug = models.SlugField(null=True)
    document_title = models.TextField(blank=True, null=True)
    document_collection = models.ForeignKey(Document_Collection, null=True)
    document_summary = models.TextField(blank=True, null=True, help_text="This is the first parage of the first page, be default")
    page_count = models.IntegerField(null=True)
    thumbnail = models.TextField(blank=True, null=True, help_text="url for image thumbnail")
    
    
    metadata = hstore.SerializedDictionaryField(null=True, help_text="Document metadata, as a dict")
    objects = hstore.HStoreManager()
    
    ## need to add: number_of_pages -- makes has_next stuff easier for pages

    def __unicode__(self):
        return "%s" % (self.document_id)
 

    def get_absolute_url(self):
        return "/documents/collection/%s/%s/" % (self.document_collection.collection_slug, self.document_id)
    
class Page(models.Model):
    doc = models.ForeignKey(Document)
    page_number = models.IntegerField(null=True)
    page_text = models.TextField(blank=True, null=True, help_text="This is the page full text")
    image = models.TextField(blank=True, null=True, help_text="url for image")
    thumbnail = models.TextField(blank=True, null=True, help_text="url for image thumbnail")
    page_dimensions = models.PolygonField(null=True, spatial_index=False, srid=97589)
    orientation = models.CharField(max_length=1, null=True, help_text="V=vertical, H=horizontal. Or do we need 4 orientations?")
    objects = models.GeoManager()

    def get_geojson_url(self):
        return "/documents/geojson/%s/%s/p%s.geojson" % (self.doc.document_collection.collection_slug, self.doc.document_id, self.page_number)
    
    def get_absolute_url(self):
        return "/documents/collection/%s/%s/%s/" % (self.doc.document_collection.collection_slug, self.doc.document_id, self.page_number)
        
    def __unicode__(self):
        return "Doc: %s page: %s" % (self.doc.document_id, self.page_number)

    class Meta:    
        unique_together = (("doc", "page_number"),)
# todo: hash the actual words, so instead of saving a word, we save an id. 

class PageWord(models.Model):
    # to save time, we're not explicitly checking that page_pk is indeed a page primary key. But it should be.
    page_pk = models.IntegerField()
    text = models.CharField(max_length=755, blank=True, null=True)
    word_num = models.IntegerField(null=True)
    line_num = models.IntegerField(null=True)
    ## bbox should be of the form 
    bbox = models.CharField(max_length=31, blank=True, null=True)
    poly = models.PolygonField(null=True, spatial_index=False, srid=97589)
    # we don't create a spatial index initially. Manage this by hand, because this will kill our inserts otherwise.
    objects = models.GeoManager()
    
    """
    After creating PageWord with syncdb, you must run manage.py drop_gis_constraints to kill some 
    unenforceable constraints. But equivalently you can just run this at the db prompt. 
    
    # todo: roll a custom srid so that the enforce_srid constraint isn't violated. 
    
    alter table documents_pageword drop constraint "enforce_srid_poly";
    alter table documents_pageword drop constraint "enforce_dims_poly";
    alter table documents_pageword drop constraint "enforce_geotype_poly";
    """

