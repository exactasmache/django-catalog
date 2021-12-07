__author__ = "Marcelo L. Bianchetti"
__license__ = "MIT License"
__version__ = "1.0.0"
__email__ = "mbianchetti at dc.uba.ar"
__status__ = "Development"

from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Q

from .serializers import BookSerializer
from .models import Book

SEARCH_KEYWORD = 'search'
PK_KEYWORD = 'pk'


@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'List': '/list/?search="some text"',
    }
    return Response(api_urls)


class CatalogViewSet(ReadOnlyModelViewSet):
    serializer_class = BookSerializer

    def get_queryset(self):
        search = self.request.query_params.get(SEARCH_KEYWORD)

        if search is None:
            return Book.objects.order_by('title')

        q_filter = Q(title__icontains=search) |\
            Q(author__last_name__icontains=search) |\
            Q(author__first_name__icontains=search)

        q = Book.objects.filter(q_filter).order_by('title')

        return q


class SimilarsViewSet(ReadOnlyModelViewSet):
    serializer_class = BookSerializer

    def get_queryset(self):
        pk = self.request.query_params.get(PK_KEYWORD)

        if pk is None:
            return Book.objects.order_by('title')

        book = Book.objects.get(id=pk)

        # All the books for the same author.
        q_filter = Q(author__id=book.author.id)

        # All the books that matches at least one title word
        for word in book.title.split():
            q_filter |= Q(title__icontains=word)

        q = Book.objects.filter(q_filter).order_by('title')

        return q
