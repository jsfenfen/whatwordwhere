from rest_framework.pagination import CursorPagination

class WWW_CursorPagination(CursorPagination):
    cursor_query_param = 'cursor'
    page_size = 100 # will this mess up csvs? 
    ordering = '-id'
    template = 'rest_framework/pagination/previous_and_next.html'