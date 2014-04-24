"""
Utilities to help create GEOS objects.
"""

from django.contrib.gis.geos import GEOSGeometry
from hocr_parser.parse_utils import get_words_from_page

def get_poly_string_from_bbox(bbox_string):
    """ Get a string formatted for GEOS based on an hocr-style bounding box"""
    coords = bbox_string.split()
    return """SRID=97589;POLYGON((%s %s, %s %s,%s %s,%s %s,%s %s))""" % (
        coords[0], coords[1], coords[0], coords[3], coords[2], 
        coords[3], coords[2], coords[1],coords[0], coords[1] 
    )
    

def get_word_shapes(word_array):
    """ Adds GEOSGeometry objects to the word array"""
    for word in word_array:
        bbox_string  = get_poly_string_from_bbox(word['bbox'])
        word['poly'] = GEOSGeometry(bbox_string)
    return word_array
    
