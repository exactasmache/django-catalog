__author__ = "Marcelo L. Bianchetti"
__license__ = "MIT License"
__version__ = "1.0.0"
__email__ = "mbianchetti at dc.uba.ar"
__status__ = "Development"

import operator
from functools import reduce

from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q

from .serializers import BookSerializer
from .models import Book

SEARCH_KEYWORD = 'search'
KEYWORDS_KEYWORD = 'keyword'
PK_KEYWORD = 'pk'


class CatalogViewSet(ReadOnlyModelViewSet):
    serializer_class = BookSerializer
    queryset = Book.objects.all()

    def get_object(self):
        pk = self.request.query_params.get(PK_KEYWORD)
        return super().get_object()

    def get_queryset(self):
        search = self.request.query_params.get(SEARCH_KEYWORD)
        keyword = self.request.query_params.get(KEYWORDS_KEYWORD)

        if search is not None:
            q_filter = Q(title__icontains=search) |\
                Q(author__last_name__icontains=search) |\
                Q(author__first_name__icontains=search)

            q = Book.objects.filter(q_filter).order_by('title')

            return q

        elif keyword is not None:
            q_filter = Q(keywords__icontains=keyword)

            q = Book.objects.filter(q_filter).order_by('title')

            return q

        else:
            return Book.objects.order_by('title')

    @action(detail=True)
    def get_similars(self, request, pk=None):

        if pk is None:
            everything = Book.objects.order_by('title')
            serializer = BookSerializer(everything, many=True)
            return Response(serializer.data)

        book = get_object_or_404(self.queryset, id=pk)

        # All the books for the same author.
        q_filter = Q(author__id=book.author.id)

        # All the books that matches at least one title word.
        title_words = book.title.split()
        q_filter |= reduce(
            operator.or_,
            (Q(title__icontains=word) for word in title_words)
        )

        # All the books sharing some of the keywords.
        keywords = book.keywords.split(', ')
        q_filter |= reduce(
            operator.or_,
            (Q(keywords__contains=word) for word in keywords)
        )

        # We do not return the selected object.
        q_filter &= ~Q(id=book.id)

        q = Book.objects.filter(q_filter).order_by('title')

        page = self.paginate_queryset(q)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(page, many=True)
        return Response(serializer.data)
