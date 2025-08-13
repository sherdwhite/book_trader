# -*- coding: utf-8 -*-

from decimal import Decimal

from books.models import Author, Book, Publisher, Rating
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TestUserViewSet(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.list_url = reverse("user-list")
        self.detail_url = reverse("user-detail", kwargs={"pk": self.user.pk})

    def test_user_list(self):
        """Test GET /api/users/ returns user list"""
        response = self.client.get(self.list_url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1  # type: ignore
        assert response.data[0]["username"] == self.user.username  # type: ignore

    def test_user_detail(self):
        """Test GET /api/users/{id}/ returns user details"""
        response = self.client.get(self.detail_url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["username"] == self.user.username  # type: ignore
        assert response.data["email"] == self.user.email  # type: ignore

    def test_user_create(self):
        """Test POST /api/users/ creates new user"""
        data = {
            "username": "newuser",
            "email": "new@example.com",
            "password": "newpass123",
        }
        response = self.client.post(self.list_url, data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(username="newuser").exists()

    def test_user_update(self):
        """Test PUT /api/users/{id}/ updates user"""
        data = {
            "username": "updateduser",
            "email": "updated@example.com",
        }
        response = self.client.put(self.detail_url, data=data)
        assert response.status_code == status.HTTP_200_OK
        self.user.refresh_from_db()
        assert self.user.username == "updateduser"

    def test_user_delete(self):
        """Test DELETE /api/users/{id}/ deletes user"""
        response = self.client.delete(self.detail_url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not User.objects.filter(pk=self.user.pk).exists()


class TestBookViewSet(APITestCase):
    def setUp(self):
        self.author = Author.objects.create(name="Test Author")
        self.publisher = Publisher.objects.create(name="Test Publisher")

        # Create books with different ratings to test ordering
        self.book1 = Book.objects.create(
            title="Book 1",
            isbn="1111111111111",
            publisher=self.publisher,
            average_rating=Decimal("3.5"),
        )
        self.book1.authors.add(self.author)

        self.book2 = Book.objects.create(
            title="Book 2",
            isbn="2222222222222",
            publisher=self.publisher,
            average_rating=Decimal("4.5"),
        )
        self.book2.authors.add(self.author)

        self.list_url = reverse("book-list")
        self.detail_url = reverse("book-detail", kwargs={"pk": self.book1.pk})

    def test_book_list_ordering(self):
        """Test GET /api/books/ returns books ordered by rating desc"""
        response = self.client.get(self.list_url)
        assert response.status_code == status.HTTP_200_OK

        books = response.data  # type: ignore
        assert len(books) == 2
        # Should be ordered by average_rating descending
        assert float(books[0]["average_rating"]) == 4.5  # book2 first
        assert float(books[1]["average_rating"]) == 3.5  # book1 second

    def test_book_detail(self):
        """Test GET /api/books/{id}/ returns book details"""
        response = self.client.get(self.detail_url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == self.book1.title  # type: ignore
        assert response.data["isbn"] == self.book1.isbn  # type: ignore

    def test_book_create_without_rating(self):
        """Test POST /api/books/ creates book with model default rating (0.0)"""
        data = {
            "title": "New Book",
            "isbn": "3333333333333",
            "authors": [self.author.pk],
            "publisher": self.publisher.pk,
            "description": "A new book",
        }
        response = self.client.post(self.list_url, data=data)
        assert response.status_code == status.HTTP_201_CREATED

        # Should have model default average_rating of 0.0
        new_book = Book.objects.get(isbn="3333333333333")
        assert new_book.average_rating == Decimal("0.0")

    def test_book_create_with_rating(self):
        """Test POST /api/books/ creates book with provided rating"""
        data = {
            "title": "New Book with Rating",
            "isbn": "4444444444444",
            "authors": [self.author.pk],
            "publisher": self.publisher.pk,
            "description": "A new book",
            "average_rating": "2.5",
        }
        response = self.client.post(self.list_url, data=data)
        assert response.status_code == status.HTTP_201_CREATED

        # Should keep the provided rating
        new_book = Book.objects.get(isbn="4444444444444")
        assert new_book.average_rating == Decimal("2.5")

    def test_book_update(self):
        """Test PUT /api/books/{id}/ updates book"""
        data = {
            "title": "Updated Book",
            "isbn": self.book1.isbn,
            "authors": [self.author.pk],
            "publisher": self.publisher.pk,
            "description": "Updated description",
            "average_rating": "3.5",
        }
        response = self.client.put(self.detail_url, data=data)
        assert response.status_code == status.HTTP_200_OK

        self.book1.refresh_from_db()
        assert self.book1.title == "Updated Book"

    def test_book_delete(self):
        """Test DELETE /api/books/{id}/ deletes book"""
        response = self.client.delete(self.detail_url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Book.objects.filter(pk=self.book1.pk).exists()


class TestRatingViewSet(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="rater", email="rater@example.com", password="testpass123"
        )
        self.author = Author.objects.create(name="Test Author")
        self.publisher = Publisher.objects.create(name="Test Publisher")
        self.book = Book.objects.create(
            title="Test Book",
            isbn="1234567890123",
            publisher=self.publisher,
            average_rating=Decimal("0.0"),
        )
        self.book.authors.add(self.author)

        self.rating = Rating.objects.create(user=self.user, book=self.book, rating=4)

        self.list_url = reverse("rating-list")
        self.detail_url = reverse("rating-detail", kwargs={"pk": self.rating.pk})

    def test_rating_list(self):
        """Test GET /api/ratings/ returns rating list"""
        response = self.client.get(self.list_url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1  # type: ignore

    def test_rating_detail(self):
        """Test GET /api/ratings/{id}/ returns rating details"""
        response = self.client.get(self.detail_url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["rating"] == 4  # type: ignore
        assert response.data["user"] == self.user.pk  # type: ignore
        assert response.data["book"] == self.book.pk  # type: ignore

    def test_rating_create_new(self):
        """Test POST /api/ratings/ creates new rating"""
        # Create another user and book for new rating
        user2 = User.objects.create_user(
            username="rater2", email="rater2@example.com", password="testpass123"
        )

        data = {"user": user2.pk, "book": self.book.pk, "rating": 5}
        self.client.post(self.list_url, data=data)

        # Verify new rating was created
        assert Rating.objects.filter(user=user2, book=self.book).exists()

    def test_rating_create_existing_updates(self):
        """Test POST /api/ratings/ updates existing rating for same user/book"""
        initial_count = Rating.objects.count()

        # Try to create rating for same user/book combination
        data = {"user": self.user.pk, "book": self.book.pk, "rating": 5}
        self.client.post(self.list_url, data=data)

        # Should update existing rating, not create new one
        assert Rating.objects.count() == initial_count
        self.rating.refresh_from_db()
        assert self.rating.rating == 5

    def test_rating_delete_updates_book_average(self):
        """Test DELETE /api/ratings/{id}/ updates book average rating"""
        # Add another rating to test average calculation
        user2 = User.objects.create_user(
            username="rater2", email="rater2@example.com", password="testpass123"
        )
        Rating.objects.create(user=user2, book=self.book, rating=2)

        # Book should have average of (4+2)/2 = 3.0
        self.book.refresh_from_db()
        assert self.book.average_rating == Decimal("3.0")

        # Delete one rating
        response = self.client.delete(self.detail_url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Book average should now be 2.0 (only remaining rating)
        self.book.refresh_from_db()
        assert self.book.average_rating == Decimal("2.0")

    def test_rating_delete_last_rating_zeros_average(self):
        """Test deleting last rating sets book average to 0"""
        # Delete the only rating
        response = self.client.delete(self.detail_url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Book average should be 0
        self.book.refresh_from_db()
        assert self.book.average_rating == Decimal("0.0")

    def test_get_object_with_pk(self):
        """Test get_object method when accessing by pk"""
        # This tests the get_object override when pk is provided
        response = self.client.get(self.detail_url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["pk"] == self.rating.pk  # type: ignore

    def test_rating_update(self):
        """Test PUT /api/ratings/{id}/ updates rating"""
        data = {"user": self.user.pk, "book": self.book.pk, "rating": 3}
        response = self.client.put(self.detail_url, data=data)
        assert response.status_code == status.HTTP_200_OK

        self.rating.refresh_from_db()
        assert self.rating.rating == 3


class TestAuthorViewSet(APITestCase):
    def setUp(self):
        self.author = Author.objects.create(name="Test Author")
        self.list_url = reverse("author-list")
        self.detail_url = reverse("author-detail", kwargs={"pk": self.author.pk})

    def test_author_list(self):
        """Test GET /api/authors/ returns author list"""
        response = self.client.get(self.list_url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1  # type: ignore

    def test_author_detail(self):
        """Test GET /api/authors/{id}/ returns author details"""
        response = self.client.get(self.detail_url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == self.author.name  # type: ignore

    def test_author_create(self):
        """Test POST /api/authors/ creates new author"""
        data = {"name": "New Author"}
        response = self.client.post(self.list_url, data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Author.objects.filter(name="New Author").exists()

    def test_author_update(self):
        """Test PUT /api/authors/{id}/ updates author"""
        data = {"name": "Updated Author"}
        response = self.client.put(self.detail_url, data=data)
        assert response.status_code == status.HTTP_200_OK
        self.author.refresh_from_db()
        assert self.author.name == "Updated Author"

    def test_author_delete(self):
        """Test DELETE /api/authors/{id}/ deletes author"""
        response = self.client.delete(self.detail_url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Author.objects.filter(pk=self.author.pk).exists()


class TestPublisherViewSet(APITestCase):
    def setUp(self):
        self.publisher = Publisher.objects.create(name="Test Publisher")
        self.list_url = reverse("publisher-list")
        self.detail_url = reverse("publisher-detail", kwargs={"pk": self.publisher.pk})

    def test_publisher_list(self):
        """Test GET /api/publishers/ returns publisher list"""
        response = self.client.get(self.list_url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1  # type: ignore

    def test_publisher_detail(self):
        """Test GET /api/publishers/{id}/ returns publisher details"""
        response = self.client.get(self.detail_url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == self.publisher.name  # type: ignore

    def test_publisher_create(self):
        """Test POST /api/publishers/ creates new publisher"""
        data = {"name": "New Publisher"}
        response = self.client.post(self.list_url, data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Publisher.objects.filter(name="New Publisher").exists()

    def test_publisher_update(self):
        """Test PUT /api/publishers/{id}/ updates publisher"""
        data = {"name": "Updated Publisher"}
        response = self.client.put(self.detail_url, data=data)
        assert response.status_code == status.HTTP_200_OK
        self.publisher.refresh_from_db()
        assert self.publisher.name == "Updated Publisher"

    def test_publisher_delete(self):
        """Test DELETE /api/publishers/{id}/ deletes publisher"""
        response = self.client.delete(self.detail_url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Publisher.objects.filter(pk=self.publisher.pk).exists()
