from django.contrib.gis.geos import GEOSGeometry

from parser.parse_utils import get_words_from_page

def get_poly_string_from_bbox(bbox_string):
    coords = bbox_string.split()
    
    
    return """POLYGON((%s %s, %s %s,%s %s,%s %s,%s %s))""" % (
        coords[0], coords[1], coords[0], coords[3], coords[2], 
        coords[3], coords[2], coords[1],coords[0], coords[1] 
    )
    

def get_word_shapes(word_array):
    """ Adds GEOSGeometry objects to the word array"""
    
    for word in word_array:
        bbox_string  = get_poly_string_from_bbox(word['bbox'])
        word['poly'] = GEOSGeometry(bbox_string)
    
    return word_array
    
