from rest_framework import generics
from util.pagination import CustomPagination

class GenericListView(generics.ListAPIView):
    pagination_class: object = CustomPagination

    def filter(self, data: object) -> object:
        return data

    def get_queryset(self) -> object:
        data = self.queryset
        return self.filter(data)