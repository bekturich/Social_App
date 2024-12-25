from rest_framework import pagination

class SavePagination(pagination.PageNumberPagination):
    page_size = 4