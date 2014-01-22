import geojson

def get_geojson_feature(id, raw_bbox_string, properties_dict):
    """ Make a geojson feature from a raw bbox string etc."""
    coords = raw_bbox_string.split()
    
    # Tesseract uses ints, but allow floats
    for i, val in enumerate(coords):
        coords[i] = float(val)
    # bbox order = # x0 y0 x1 y1
    
    bbox_json_obj = geojson.Polygon([[
        (coords[0], coords[1]), 
        (coords[0], coords[3]), 
        (coords[2], coords[3]), 
        (coords[2], coords[1]),
        (coords[0], coords[1])
    ]])
    return geojson.Feature(id, bbox_json_obj, properties=properties_dict)



def get_feature_collection(page):
    """ Handle a buncha words"""
    feature_array = []
    for i,word in enumerate(page['words']):
        # should line_num be required here? It's not supported by -bbox output... 
        word_properties = {'word':word['text'], 'line_num':word['line_num']}
        # should we instead rely on the the word number for the id? 
        feature_array.append(get_geojson_feature(i, word['bbox'], word_properties))
        
    featurecollection = geojson.FeatureCollection(feature_array)
    return geojson.dumps(featurecollection)