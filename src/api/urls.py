__author__ = "Marcelo L. Bianchetti"
__license__ = "MIT License"
__version__ = "1.0.0"
__email__ = "mbianchetti at dc.uba.ar"
__status__ = "Development"

from django.urls import path
from django.conf.urls import url
from django.urls.conf import re_path
from . import views

from .views import CatalogViewSet, SimilarsViewSet


urlpatterns = [
    path('', views.apiOverview, name='api-overview'),
    url(r'^list/$', CatalogViewSet.as_view({'get': 'list'})),
    url(r'^list/similars/$', SimilarsViewSet.as_view({'get': 'list'})),
]
