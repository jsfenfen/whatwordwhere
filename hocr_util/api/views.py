from django.shortcuts import render


from rest_framework import viewsets
from rest_framework import generics


from rest_framework.settings import api_settings
from paginated_csv_renderer import PaginatedCSVRenderer

from documents.models import Page, PageWord
from api.serializers import PageSerializer, PageWordSerializer
from api.filters import PageFilter, PageWordFilter, OrderingFilter

class alternatelypaginatedviewset(viewsets.ReadOnlyModelViewSet):
    def get_paginate_by(self):
        """
        Use smaller pagination for json/html than csv
        As per settings.py, default is 10, max is 100, param is page_size
        For csv you get 2000 rows.
        """
        if self.request.accepted_renderer.format.lower() == ('csv'):
            return CSV_PAGE_SIZE
        else:
            superclass = super(viewsets.ReadOnlyModelViewSet, self)
            return superclass.get_paginate_by(superclass)


page_orderable_fields = ['page_number']



class PageViewSet(alternatelypaginatedviewset):
    """
    API endpoint that allows new filings to be viewed.
    """
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES + [PaginatedCSVRenderer] 

    # processing the header makes most of these not zero. 
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    filter_class = PageFilter
    

    def get_queryset(self):  
        # It seems like there should be a better way to chain filters together than this
        # the django-rest-framework viewset approach appear to allow just one filter though
        # so just apply these filters before the filter_class sees it. 

        self.queryset = OrderingFilter(self.queryset, self.request.GET, page_orderable_fields)

        return self.queryset



page_word_orderable_fields = ['page_pk', 'line_num', 'word_num']

class PageWordViewSet(alternatelypaginatedviewset):
    """
    API endpoint that allows new filings to be viewed.
    """
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES + [PaginatedCSVRenderer] 

    # processing the header makes most of these not zero. 
    queryset = PageWord.objects.all()
    serializer_class = PageWordSerializer
    filter_class = PageWordFilter

    def get_queryset(self):  
        # It seems like there should be a better way to chain filters together than this
        # the django-rest-framework viewset approach appear to allow just one filter though
        # so just apply these filters before the filter_class sees it. 

        self.queryset = OrderingFilter(self.queryset, self.request.GET, page_word_orderable_fields)

        return self.queryset