from rest_framework_csv.renderers import CSVRenderer


# Thanks to @mjumbewu this makes CSVRenderer work for paginated stuff; https://gist.github.com/mjumbewu/6639263
class PaginatedCSVRenderer(CSVRenderer):
    results_field = 'results'
 
    def render(self, data, media_type=None, renderer_context=None):
        if not isinstance(data, list):
            data = data.get(self.results_field, [])
        return super(PaginatedCSVRenderer, self).render(data, media_type, renderer_context)