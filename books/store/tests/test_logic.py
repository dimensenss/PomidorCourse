from unittest import TestCase

from django.contrib.auth.models import User

from store.logic import set_rate
from store.models import Book, UserBookRelation


class RateLogicTestCase(TestCase):
    def setUp(self):
        self.owner = User.objects.create(username='test_owner11', first_name='Test1', last_name='Owner')
        self.reader = User.objects.create(username='test_reader11', first_name='Test2', last_name='Reader')

        self.book_1 = Book.objects.create(name='Book 799', price=25, author_name='test', owner=self.owner)
        self.book_2 = Book.objects.create(name='Book 2', price=55, author_name='test2')

        UserBookRelation.objects.create(user=self.reader, book=self.book_1, like=True, rate=5)
        UserBookRelation.objects.create(user=self.owner, book=self.book_2, like=True, rate=4)
        user_book_rel_3 = UserBookRelation.objects.create(user=self.reader, book=self.book_2, like=True)
        user_book_rel_3.rate = 3
        user_book_rel_3.save()

    def test_set_rate(self):
        set_rate(self.book_2)

