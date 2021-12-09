__author__ = "Marcelo L. Bianchetti"
__license__ = "MIT License"
__version__ = "1.0.0"
__email__ = "mbianchetti at dc.uba.ar"
__status__ = "Development"

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from .models import Author, Book

import datetime


class AuthorTestCase(APITestCase):
    def setUp(self):
        '''
            Initializes the catalog with 3 authors and 7 books.
            It also initializes a client to test the API.
            It is accessible via self.client.
        '''
        Author.objects.create(
            first_name="Julio",
            last_name="Verne",
            date_of_birth=datetime.date.today()
        )
        Author.objects.create(
            first_name="Emilio",
            last_name="Salgari",
            date_of_birth=datetime.date.today()
        )
        Author.objects.create(
            first_name="Agatha",
            last_name="Christie",
            date_of_birth=datetime.date.today()
        )
        books = [
            (
                "La vuelta al mundo en 80 días",
                datetime.date.today(),
                1,
                "Aventura, viajes, ficción"
            ),
            (
                "Viaje al centro de la tierra",
                datetime.date.today(),
                1,
                "Aventura, viajes, ficción"
            ),
            (
                "Sandokán",
                datetime.date.today(),
                2,
                "Aventura, viajes, barcos, batallas, piratas, amor, amistad"
            ),
            (
                "Cartago en llamas",
                datetime.date.today(),
                2,
                "Aventura, batallas, guerra, heroes"
            ),
            (
                "El corsario negro",
                datetime.date.today(),
                2,
                "Aventura, viajes, barcos, batallas, piratas, amor, amistad"
            ),
            (
                "El misterioso señor Brown",
                datetime.date.today(),
                3,
                "Detectives, policial, aventura, drama, misterio"
            ),
            (
                "El asesinato de Roger Acroyd",
                datetime.date.today(),
                3,
                "Detectives, policial, aventura, misterio, médico"
            ),
        ]
        for book in books:
            Book.objects.create(
                title=book[0],
                date_of_publication=book[1],
                author_id=book[2],
                keywords=book[3]
            )
        self.client = APIClient()

    def test_API_list_all(self):
        '''Tests listing all the elements.'''

        url = '/api/list/'
        response = self.client.get(url)

        data = response.data

        keys = set(['count', 'next', 'previous', 'results'])
        assert(keys == set(data.keys()))

        assert(data['count'] == 7)
        assert(data['previous'] is None)
        assert(data['next'] is None)

        keys = set([
            'id',
            'title',
            'date_of_publication',
            'author',
            'keywords'
        ])

        for res in data['results']:
            assert(set(res.keys()) == keys)

        ids = set(range(1, 8))
        r_ids = {r['id'] for r in data['results']}

        assert(ids == r_ids)

        assert(data['results'][0]['id'] == 4)

    def test_API_list_retrieve_one(self):
        '''Tests retriving only one element.'''

        book_id = 4
        url = f'/api/list/{book_id}/'
        response = self.client.get(url)

        data = response.data

        keys = set([
            'id',
            'title',
            'date_of_publication',
            'author',
            'keywords'
        ])
        assert(keys == set(data.keys()))

        assert(data['id'] == book_id)

        r_keywords = set(data['keywords'].split(', '))
        keywords = set(['Aventura', 'batallas', 'guerra', 'heroes'])
        assert(r_keywords == keywords)

    def test_API_list_keyword(self):
        '''Tests keyword search.'''

        keyword = 'médico'
        url = f'/api/list/?keyword={keyword}'
        response = self.client.get(url)

        data = response.data

        keys = set(['count', 'next', 'previous', 'results'])
        assert(keys == set(data.keys()))

        assert(data['count'] == 1)
        assert(data['previous'] is None)
        assert(data['next'] is None)

        keys = set([
            'id',
            'title',
            'date_of_publication',
            'author',
            'keywords'
        ])

        for res in data['results']:
            assert(set(res.keys()) == keys)

        assert(data['results'][0]['id'] == 7)

    def test_API_similars(self):
        '''Tests listing similar elements.'''
        
        book_id = 5
        url = f'/api/similars/{book_id}/'
        response = self.client.get(url)

        data = response.data

        keys = set(['count', 'next', 'previous', 'results'])
        assert(keys == set(data.keys()))

        assert(data['count'] == 6)
        assert(data['previous'] is None)
        assert(data['next'] is None)

        keys = set([
            'id',
            'title',
            'date_of_publication',
            'author',
            'keywords'
        ])

        for res in data['results']:
            assert(set(res.keys()) == keys)

        ids = {1, 2, 3, 4, 6, 7}
        r_ids = {r['id'] for r in data['results']}
        assert(ids == r_ids)

        assert(data['results'][0]['id'] == 4)
