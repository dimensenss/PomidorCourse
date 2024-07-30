from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from store.models import Book
from store.serializers import BookSerializer


class APITestCase(APITestCase):
    def test_get(self):
        book_1 = Book.objects.create(name='Book 1', price=25)
        book_2 = Book.objects.create(name='Book 2', price=55)
        url = reverse('book-list')

        response = self.client.get(url)
        serializer = BookSerializer([book_1, book_2], many=True)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data, serializer.data)
