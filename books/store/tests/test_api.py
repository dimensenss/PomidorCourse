from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from store.models import Book
from store.serializers import BookSerializer


class BooksAPITestCase(APITestCase):
    def setUp(self):
        self.book_1 = Book.objects.create(name='Book A', price=25, author_name='Author_A')
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
