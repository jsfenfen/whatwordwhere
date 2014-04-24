""" Django models for document, pages, and words on pages (page_words).
    Assumes the db uses utf-8 encoding
"""

from django.contrib.gis.db import models

class Document(models.Model):
    document_id = models.CharField(max_length=63, blank=True, null=True, unique=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    year = models.IntegerField(null=True)
    month = models.IntegerField(null=True)
    form = models.CharField(max_length=7, blank=True, null=True)
    
    def get_absolute_url(self):
        return "/documents/document/%s/" % (self.document_id)
    
class Page(models.Model):
    doc = models.ForeignKey(Document)
    page_number = models.IntegerField(null=True)
    image = models.CharField(max_length=15, blank=True, null=True)
    page_dimensions = models.PolygonField(null=True, spatial_index=False, srid=97589)
    orientation = models.CharField(max_length=1, null=True, help_text="V=vertical, H=horizontal. Or do we need 4 orientations?")
    objects = models.GeoManager()

    def get_geojson_url(self):
        return "/documents/geojson/%s/p%s.geojson" % (self.doc.document_id, self.page_number)

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

