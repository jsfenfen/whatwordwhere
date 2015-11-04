import django_filters

from datetime import date, timedelta
from documents.models import Page

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
