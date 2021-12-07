__author__ = "Marcelo L. Bianchetti"
__license__ = "MIT License"
__version__ = "1.0.0"
__email__ = "mbianchetti at dc.uba.ar"
__status__ = "Development"

from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import BookSerializer
from .models import Book


@api_view(['GET'])
def apiOverview(request):
    api_urls = {
      'List': '/<catalog>/',
    }
    return Response(api_urls)


class CatalogViewSet(ModelViewSet):
    serializer_class = BookSerializer

    def get_object(self):
        print("Getting", self)
        return get_object_or_404(Book, id=self.request.query_params.get("id"))

    def get_queryset(self):
        return Book.objects.order_by('title')
