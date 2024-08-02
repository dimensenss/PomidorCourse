import json

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from store.models import Book
from store.serializers import BookSerializer


class BooksAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='Test User')
        self.book_1 = Book.objects.create(name='Book A', price=25, author_name='Author_A', owner=self.user)
        self.book_2 = Book.objects.create(name='Book B', price=55, author_name='Author_B')
        self.book_3 = Book.objects.create(name='Book about Author_B', price=65, author_name='Author_C')

    def test_get(self):
        url = reverse('book-list')
        response = self.client.get(url)
        serializer = BookSerializer([self.book_1, self.book_2, self.book_3], many=True)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data, serializer.data)

    def test_filter(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'price': '55.00'})
        serializer = BookSerializer([self.book_2], many=True)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data, serializer.data)

    def test_search(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'search': 'Author_B'})
        serializer = BookSerializer([self.book_2, self.book_3], many=True)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data, serializer.data)

    def test_ordering(self):
        url = reverse('book-list')
        response_sort_by_price = self.client.get(url, data={'ordering': 'price'})
        response_sort_by_desc_price = self.client.get(url, data={'ordering': '-price'})
        response_sort_by_author = self.client.get(url, data={'ordering': 'author_name'})
        response_sort_by_desc_author = self.client.get(url, data={'ordering': '-author_name'})

        excepted_data_sort_by_price = BookSerializer([self.book_1, self.book_2, self.book_3], many=True)
        excepted_data_sort_by_desc_price = BookSerializer([self.book_3, self.book_2, self.book_1], many=True)
        excepted_data_sort_by_author = BookSerializer([self.book_1, self.book_2, self.book_3], many=True)
        excepted_data_sort_by_desc_author = BookSerializer([self.book_3, self.book_2, self.book_1], many=True)

        self.assertEqual(status.HTTP_200_OK, response_sort_by_price.status_code)
        self.assertEqual(status.HTTP_200_OK, response_sort_by_desc_price.status_code)
        self.assertEqual(status.HTTP_200_OK, response_sort_by_author.status_code)
        self.assertEqual(status.HTTP_200_OK, response_sort_by_desc_author.status_code)

        self.assertEqual(response_sort_by_price.data, excepted_data_sort_by_price.data)
        self.assertEqual(response_sort_by_desc_price.data, excepted_data_sort_by_desc_price.data)
        self.assertEqual(response_sort_by_author.data, excepted_data_sort_by_author.data)
        self.assertEqual(response_sort_by_desc_author.data, excepted_data_sort_by_desc_author.data)

    def test_create(self):
        url = reverse('book-list')
        self.client.force_login(self.user)
        data = {
            "name": "Test Book",
            "price": 100,
            "author_name": "Test Author"
        }
        json_data = json.dumps(data)

        self.assertEqual(3, Book.objects.all().count())
        response = self.client.post(url, data=json_data, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(4, Book.objects.all().count())
        self.assertEqual(self.user, Book.objects.last().owner)
        print(Book.objects.last().owner)

    def test_update(self):
        url = reverse('book-detail', args=(self.book_1.id,))
        self.client.force_login(self.user)
        data = {
            "name": self.book_1.name,
            "price": 797,
            "author_name": self.book_1.author_name
        }
        json_data = json.dumps(data)
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.book_1.refresh_from_db()
        self.assertEqual(data['price'], self.book_1.price)

    def test_not_owner_update(self):
        self.user2 = User.objects.create_user(username='Test User2')
        url = reverse('book-detail', args=(self.book_1.id,))
        self.client.force_login(self.user2)
        data = {
            "name": self.book_1.name,
            "price": 797,
            "author_name": self.book_1.author_name
        }
        json_data = json.dumps(data)
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.book_1.refresh_from_db()
        self.assertEqual(25, self.book_1.price)

        self.assertEqual(response.data, {
            'detail': ErrorDetail(string='You do not have permission to perform this action.',
                                  code='permission_denied')})

    def test_not_owner_but_staff_update(self):
        self.user2 = User.objects.create_user(username='Test User2', is_staff=True)
        url = reverse('book-detail', args=(self.book_1.id,))
        self.client.force_login(self.user2)
        data = {
            "name": self.book_1.name,
            "price": 797,
            "author_name": self.book_1.author_name
        }
        json_data = json.dumps(data)
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.book_1.refresh_from_db()
        self.assertEqual(data['price'], self.book_1.price)



    def test_delete(self):
        url = reverse('book-detail', args=(self.book_1.id,))
        self.client.force_login(self.user)

        self.assertEqual(3, Book.objects.all().count())
        response_del = self.client.delete(url, content_type='application/json')

        self.assertEqual(response_del.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(2, Book.objects.all().count())

        response_get = self.client.get(url, content_type='application/json')
        self.assertEqual(response_get.status_code, status.HTTP_404_NOT_FOUND)

    def test_not_owner_delete(self):
        self.user2 = User.objects.create_user(username='Test User2')
        url = reverse('book-detail', args=(self.book_1.id,))
        self.client.force_login(self.user2)

        self.assertEqual(3, Book.objects.all().count())
        response_del = self.client.delete(url, content_type='application/json')

        self.assertEqual(response_del.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(3, Book.objects.all().count())

        response_get = self.client.get(url, content_type='application/json')
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)