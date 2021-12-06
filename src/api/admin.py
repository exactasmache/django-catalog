__author__ = "Marcelo L. Bianchetti"
__license__ = "MIT License"
__version__ = "1.0.0"
__email__ = "mbianchetti at dc.uba.ar"
__status__ = "Development"

from django.contrib import admin

from .models import Author, Book


admin.site.register(Author)
admin.site.register(Book)
