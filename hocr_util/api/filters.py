import django_filters
from rest_framework import filters

from datetime import date, timedelta
from documents.models import Page, PageWord

from geo_utils.filter_helpers import get_polygon

from rest_framework_gis.filterset import GeoFilterSet

from rest_framework import filters

from django.contrib.gis.geos import Polygon


# from django.db.models import Q



class PageFilter(django_filters.FilterSet):
    
    # can create both ends of a range like this: 
    #min_raised = django_filters.NumberFilter(name='tot_raised', lookup_type='gte')
    #min_spent = django_filters.NumberFilter(name='tot_spent', lookup_type='gte')
    #min_coh = django_filters.NumberFilter(name='coh_end', lookup_type='gte')

    
    #filed_before = django_filters.DateFilter(name='filed_date', lookup_type='lte') 
    #filed_after = django_filters.DateFilte    r(name='filed_date', lookup_type='gte') 
    

    class Meta:
        model = Page
        fields = ['doc', 'page_number', 'image', 'thumbnail']


class PageWordFilter(GeoFilterSet):

    #contains_geom = GeometryFilter(name='poly', lookup_type='contains')
    
    class Meta:
        model = PageWord
        fields = ['page_pk', 'text', 'word_num', 'line_num', 'poly']

def OrderingFilter(queryset, querydict, fields):
    """
    Only works if the ordering hasn't already been set. Which it hasn't, but... 
    """
    try:
        ordering=querydict['ordering']
        if ordering.lstrip('-') in fields:
            orderlist = [ordering]
            queryset = queryset.order_by(*orderlist)

    except KeyError:
        pass

    return queryset


def bbox_Filter(queryset, querydict):
    try:
        [x0,y0,x1,y1]=get_polygon(querydict['bbox'])
        
        bounding_box_poly = Polygon( ((x0,y0), (x0, y1), (x1, y1), (x1, y0), (x0, y0)) , srid=-1)
        print "\n\n\n\n" + str(bounding_box_poly)  + "\n\n\n\n"
        queryset = queryset.filter(poly__bboverlaps=bounding_box_poly)
        #queryset = queryset.filter(Q(coverage_from_date__gte=date(year,1,1), coverage_to_date__lte=date(year,12,31)))

    except (KeyError, ValueError):
        pass
    return queryset