__author__ = "Marcelo L. Bianchetti"
__license__ = "MIT License"
__version__ = "1.0.0"
__email__ = "mbianchetti at dc.uba.ar"
__status__ = "Development"

from django.urls import path
from django.views.generic import RedirectView
from django.conf.urls import url

from . import views


urlpatterns = [
    path('', views.list, name='list'),
    url(r'^favicon\.ico$', RedirectView.as_view(
        url='/static/frontend/images/favicon.ico')
        ),
]
