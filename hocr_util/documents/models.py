# assumes db uses utf-8 encoding

#from dateutil.parser import parse as dateparse
from django.contrib.gis.db import models



class Document(models.Model):
    document_id = models.CharField(max_length=63, blank=True, null=True, unique=True)
    ein = models.CharField(max_length=15, blank=True, null=True)
    year = models.IntegerField(null=True)
    month = models.IntegerField(null=True)
    form = models.CharField(max_length=7, blank=True, null=True)
    
    
class Page(models.Model):
    doc = models.ForeignKey(Document)
    page_number = models.IntegerField(null=True)
    image = models.CharField(max_length=15, blank=True, null=True)
    page_dimensions = models.PolygonField(null=True, spatial_index=False)
    orientation = models.CharField(max_length=1, null=True, help_text="V=vertical, H=horizontal. Or do we need 4 orientations?")
    objects = models.GeoManager()


# todo: hash the actual words, so instead of saving a word, we save an id. 
# Need to make it not check srid until we find one that works better
## alter table documents_pageword drop constraint "enforce_srid_bbox";
# also drop other constraints that aren't gonna be violated--we hope
## alter table documents_pageword drop constraint "enforce_dims_bbox"
## alter table documents_pageword drop constraint "enforce_geotype_bbox"


# Also todo: add an int for word_number based on the wordid; also possibly line number?
class PageWord(models.Model):
    # to save time, we're not explicitly checking that page_pk is indeed a page primary key. But it should be.
    page_pk = models.IntegerField()
    word = models.CharField(max_length=755, blank=True, null=True)
    word_num = models.IntegerField(null=True)
    line_num = models.IntegerField(null=True)
    bbox = models.PolygonField(null=True, spatial_index=False)
    # we don't create a spatial index initially. Manage this by hand, because this will kill our inserts otherwise.
    objects = models.GeoManager()
    


""" manual flush
delete from documents_page;
delete from documents_pageword;
delete from documents_document;

"""