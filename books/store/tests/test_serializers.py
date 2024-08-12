from django.contrib.auth.models import User
from django.db.models import Count, F, Avg, Q
from django.test import TestCase

from store.models import Book, UserBookRelation
from store.serializers import BookSerializer


class BookSerializerTestCase(TestCase):
    def setUp(self):
        self.owner = User.objects.create(username='test_owner', first_name='Test1', last_name='Owner')
        self.reader = User.objects.create(username='test_reader', first_name='Test2', last_name='Reader')

        self.book_1 = Book.objects.create(name='Book 799', price=25, author_name='test', owner=self.owner)
        self.book_2 = Book.objects.create(name='Book 2', price=55, author_name='test2')

        UserBookRelation.objects.create(user=self.reader, book=self.book_1, like=True)
        UserBookRelation.objects.create(user=self.owner, book=self.book_2, like=True, rate=4)
        UserBookRelation.objects.create(user=self.reader, book=self.book_2, like=True)

    def test_serializer_ok(self):
        books = Book.objects.all().annotate(
            annotated_likes=Count('userbookrelation__like', filter=Q(userbookrelation__like=True)),
            owner_name=F('owner__username'),
            rating=Avg('userbookrelation__rate'),
        ).prefetch_related(
            'readers').order_by('id')
        serializer_data = BookSerializer(books, many=True).data

        expected_data = [
            {
                'id': self.book_1.id,
                'name': 'Book 799',
                'price': '25.00',
                'author_name': 'test',
                'annotated_likes': 1,
                'owner_name': self.owner.username,
                'rating': None,
                'readers': [
                    {
                        'first_name': self.reader.first_name,
                        'last_name': self.reader.last_name,
                    }
                ]
            },
            {
                'id': self.book_2.id,
                'name': 'Book 2',
                'price': '55.00',
                'author_name': 'test2',
                'annotated_likes': 2,
                'owner_name': None,
                'rating': '4.00',
                'readers': [
                    {
                        'first_name': self.owner.first_name,
                        'last_name': self.owner.last_name,
                    },
                    {
                        'first_name': self.reader.first_name,
                        'last_name': self.reader.last_name,
                    }
                ]
            },
        ]
        self.assertEqual(serializer_data, expected_data)
