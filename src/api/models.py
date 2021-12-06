__author__ = "Marcelo L. Bianchetti"
__license__ = "MIT License"
__version__ = "1.0.0"
__email__ = "mbianchetti at dc.uba.ar"
__status__ = "Development"

from django.db import models
from django.core.validators import RegexValidator


class Author(models.Model):
    first_name = models.CharField(max_length=50, blank=False, null=False)
    last_name = models.CharField(max_length=30, blank=False, null=False)
    date_of_birth = models.DateField()

    created = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = (('first_name', 'last_name', 'date_of_birth'))

    def __str__(self) -> str:
        return f'{self.last_name}, {self.first_name}'


class Book(models.Model):
    title = models.CharField(max_length=200, blank=False, null=False)
    date_of_publication = models.DateField(blank=False, null=False)
    author = models.ForeignKey('Author', on_delete=models.CASCADE, null=False)
    keywords = models.CharField(max_length=200, validators=[
        RegexValidator(
            r'([a-zA-Z]+)(,\s[a-zA-Z]+)*',
            message='Keywords must follow the format:'
            'word_1, word_2, ..., word_k'
        )])

    created = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.title}; by {self.author}'
