from documents.models import Page
from rest_framework_gis import serializers


"""
class PageSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Page
        fields = ('page_number', 'image', 'thumbnail', 'doc')

"""

class PageSerializer(gis_serializers.GeoFeatureModelSerializer):

    class Meta:
        model = Page
        geo_field = "page_dimensions"
        fields = ('page_number', 'image', 'thumbnail', 'doc', 'page_dimensions')
