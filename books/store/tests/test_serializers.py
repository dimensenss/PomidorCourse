from django.contrib.auth.models import User
from django.test import TestCase

from store.models import Book
from store.serializers import BookSerializer


class BookSerializerTestCase(TestCase):
    def setUp(self):
        self.owner = User.objects.create(username='test_owner')
        self.reader = User.objects.create(username='test_reader')
        self.book_1 = Book.objects.create(name='Book 799', price=25, author_name='test', owner=self.owner)
        self.book_1.readers.set([self.reader])  # Use set() to set the readers

        self.book_2 = Book.objects.create(name='Book 2', price=55, author_name='test2', owner=self.owner)
        self.book_2.readers.set([self.reader])  # Use set() to set the readers

    def test_serializer_ok(self):
        serializer_data = BookSerializer([self.book_1, self.book_2], many=True).data

        expected_data = [
            {
                'id': self.book_1.id,
                'name': 'Book 799',
                'price': '25.00',
                'author_name': 'test',
                'owner': self.owner.id,  # Expect the owner ID, not the object
                'readers': [self.reader.id],  # Expect a list of reader IDs
            },
            {
                'id': self.book_2.id,
                'name': 'Book 2',
                'price': '55.00',
                'author_name': 'test2',
                'owner': self.owner.id,  # Expect the owner ID, not the object
                'readers': [self.reader.id],  # Expect a list of reader IDs
            },
        ]
        self.assertEqual(serializer_data, expected_data)
