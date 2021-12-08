__author__ = "Marcelo L. Bianchetti"
__license__ = "MIT License"
__version__ = "1.0.0"
__email__ = "mbianchetti at dc.uba.ar"
__status__ = "Development"

from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q

from .serializers import BookSerializer
from .models import Book

SEARCH_KEYWORD = 'search'
PK_KEYWORD = 'pk'


class CatalogViewSet(ReadOnlyModelViewSet):
    serializer_class = BookSerializer
    queryset = Book.objects.all()

    def get_object(self):
        pk = self.request.query_params.get(PK_KEYWORD)
        return super().get_object()

    def get_queryset(self):
        search = self.request.query_params.get(SEARCH_KEYWORD)

        if search is None:
            return Book.objects.order_by('title')

        q_filter = Q(title__icontains=search) |\
            Q(author__last_name__icontains=search) |\
            Q(author__first_name__icontains=search)

        q = Book.objects.filter(q_filter).order_by('title')

        return q

    @action(detail=True)
    def get_similars(self, request, pk=None):

        if pk is None:
            everything = Book.objects.order_by('title')
            serializer = BookSerializer(everything, many=True)
            return Response(serializer.data)

        book = get_object_or_404(self.queryset, id=pk)

        # All the books for the same author.
        q_filter = Q(author__id=book.author.id)

        # All the books that matches at least one title word
        for word in book.title.split():
            q_filter |= Q(title__icontains=word)

        q = Book.objects.filter(q_filter).order_by('title')

        paginated = self.paginate_queryset(q)
        serializer = BookSerializer(paginated, many=True)

        return Response(serializer.data)
