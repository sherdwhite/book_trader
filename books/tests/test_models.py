# encoding: utf-8
from django.contrib.auth.models import User
from django.test import TestCase

from books.models import Book, Author, Publisher, Rating


class TestBooks(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name="Óoly Y")
        self.publisher = Publisher.objects.create(name="Samsara")
        self.book = Book.objects.create(
            title="The Road of the Rune",
            isbn="1234567890123",
            publisher=self.publisher,
        )
        self.user = User.objects.create_user(
            username="A Reader",
            email="hi@example.com",
            password="h0wdy**",
        )
        self.user2 = User.objects.create_user(
            username="B Reader",
            email="hi2@example.com",
            password="h0wdy**2",
        )

    def test_average_rating(self):
        """book.average_rating should return the average rating of the book"""
        expected_rating = 3.0

        Rating.objects.create(book=self.book, user=self.user, rating=1)
        Rating.objects.create(book=self.book, user=self.user2, rating=5)
        updated_average_rating = Book.objects.get(id=self.book.id).average_rating

        assert updated_average_rating == expected_rating
