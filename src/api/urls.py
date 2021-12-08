__author__ = "Marcelo L. Bianchetti"
__license__ = "MIT License"
__version__ = "1.0.0"
__email__ = "mbianchetti at dc.uba.ar"
__status__ = "Development"

from django.urls import path, include
from rest_framework import routers

from .views import CatalogViewSet


router = routers.DefaultRouter()
router.register(r'list', CatalogViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('similars/<int:pk>/', CatalogViewSet.as_view({'get': 'get_similars'}))
]
