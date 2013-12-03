
from django.core.management.base import BaseCommand, CommandError

from parser.document_parser import document_parser
from parser.parse_utils import get_words_from_page
from geo_utils.word_shapes import get_word_shapes

class Command(BaseCommand):
    help = "test by loading a document"
    requires_model_validation = False

    def handle(self, *args, **options):
        """ test cmd to just get a page with geosgeometries attached """
        this_file = "parser/test_hocr/58-1723645_990_201204.html"
        parser = document_parser(this_file, encoding='latin-1')
        first_page = parser.next_document()
        page = get_words_from_page(first_page.getvalue())
        page['words'] = get_word_shapes(page['words'])
        