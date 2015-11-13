
def get_polygon(query_dict_polygon):
    """ Expect a bounding box in the form of x0,y0,x1,y1, return none otherwise """
    results = [int(x) for x in query_dict_polygon.split(",")]
    return results
    
    #return None