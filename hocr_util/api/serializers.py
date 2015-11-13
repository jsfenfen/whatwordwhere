from documents.models import Page, PageWord
from rest_framework_gis import serializers


"""
class PageSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Page
        fields = ('page_number', 'image', 'thumbnail', 'doc')

"""

class PageSerializer(serializers.GeoFeatureModelSerializer):

    class Meta:
        model = Page
        geo_field = 'page_dimensions'
        fields = ('page_number', 'image', 'thumbnail', 'doc', 'page_dimensions')
        # pass the overall page size as the "bounding box" 

class PageWordSerializer(serializers.GeoFeatureModelSerializer):

    class Meta:
        model = PageWord
        geo_field = 'poly'
        fields = ('page_pk', 'text', 'word_num', 'line_num', 'poly')
