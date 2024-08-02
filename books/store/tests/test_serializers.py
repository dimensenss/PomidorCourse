from django.test import TestCase

from store.models import Book
from store.serializers import BookSerializer


class BookSerializerTestCase(TestCase):
    def setUp(self):
        self.book_1 = Book.objects.create(name='Book 799', price=25, author_name='test')
        self.book_2 = Book.objects.create(name='Book 2', price=55, author_name='test2')

    def test_serializer_ok(self):
        serializer_data = BookSerializer([self.book_1, self.book_2], many=True).data
        expected_data = [
            {
                'id': self.book_1.id,
                'name': 'Book 799',
                'price': '25.00',
                'author_name': 'test',
            },
            {
                'id': self.book_2.id,
                'name': 'Book 2',
                'price': '55.00',
                'author_name': 'test2',
            },
        ]
        self.assertEqual(serializer_data, expected_data)
