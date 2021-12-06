__author__ = "Marcelo L. Bianchetti"
__license__ = "MIT License"
__version__ = "1.0.0"
__email__ = "mbianchetti at dc.uba.ar"
__status__ = "Development"

from django.urls import path
from django.conf.urls import url
from . import views

from .views import CatalogViewSet

urlpatterns = [
    path('', views.apiOverview, name='api-overview'),
    url(r'^book$', CatalogViewSet.as_view(
        {
            'get': 'retrieve',
            'post': 'create',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy'
        }
    )),
    url(r'^list/all$', CatalogViewSet.as_view(
        {
            'get': 'list',
        }
    )),
]
