__author__ = "Marcelo L. Bianchetti"
__license__ = "MIT License"
__version__ = "1.0.0"
__email__ = "mbianchetti at dc.uba.ar"
__status__ = "Development"

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


@api_view(['GET'])
def list_all(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)
