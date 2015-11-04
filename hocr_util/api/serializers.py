from documents.models import Page
from rest_framework import serializers


class PageSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Page
        fields = ('page_number', 'image', 'thumbnail', 'doc')
