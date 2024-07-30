from unittest import TestCase

from store.models import Book
from store.serializers import BookSerializer


class BookSerializerTestCase(TestCase):
    def test_serializer_ok(self):
        book_1 = Book.objects.create(name='Book 1', price=25)
        book_2 = Book.objects.create(name='Book 2', price=55)

        serializer_data = BookSerializer([book_1, book_2], many=True).data
        expected_data = [
            {
                'id': book_1.id,
                'name': 'Book 1',
                'price': '25.00',
            },
            {
                'id': book_2.id,
                'name': 'Book 2',
                'price': '55.00',
            },
        ]
        self.assertEqual(serializer_data, expected_data)
