from documents.models import Page, PageWord
from rest_framework import serializers as base_serializers
from rest_framework_gis import serializers


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        fields = self.context['request'].query_params.get('fields')
        if fields:
            fields = fields.split(',')
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)


# We can pass a fields param in to show which fields we want, but! 'id' and 'page_dimensions' are required to be output
# id is used for cursor-based pagination; geo stuff needs page_dimensions
class PageSerializer(serializers.GeoFeatureModelSerializer, DynamicFieldsModelSerializer):
    text_start = base_serializers.SerializerMethodField('get_the_text_start')
    
    absolute_url = base_serializers.ReadOnlyField(source='get_absolute_url')
    geojson_url = base_serializers.ReadOnlyField(source='get_geojson_url')

    class Meta:
        model = Page
        geo_field = 'page_dimensions'
        fields = ('id', 'page_number', 'image', 'thumbnail', 'doc', 'page_dimensions', 'text_start', 'absolute_url', 'geojson_url')
        # pass the overall page size as the "bounding box" 
    
    def get_the_text_start(self,obj):
        return obj.page_text[:200]

# also see http://stackoverflow.com/a/19145525 

# same as above
class PageWordSerializer(serializers.GeoFeatureModelSerializer, DynamicFieldsModelSerializer):

    class Meta:
        model = PageWord
        geo_field = 'poly'
        fields = ('id', 'page_pk', 'text', 'word_num', 'line_num', 'poly')
