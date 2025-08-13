from api.serializers import (
    AuthorSerializer,
    BookSerializer,
    PublisherSerializer,
    RatingSerializer,
    UserSerializer,
)
from books.models import Author, Book, Publisher, Rating
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Avg
from rest_framework import viewsets


class UserViewSet(viewsets.ModelViewSet):
    """API endpoint that allows users to be viewed or edited."""

    queryset = User.objects.all()
    serializer_class = UserSerializer


class BookViewSet(viewsets.ModelViewSet):
    """API endpoint that allows books to be viewed or edited."""

    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_queryset(self):
        queryset = super(BookViewSet, self).get_queryset()

        queryset = queryset.order_by("-average_rating")
        return queryset


class AuthorViewSet(viewsets.ModelViewSet):
    """API endpoint that allows authors to be viewed or edited."""

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class PublisherViewSet(viewsets.ModelViewSet):
    """API endpoint that allows publishers to be viewed or edited."""

    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer


class RatingViewSet(viewsets.ModelViewSet):
    """API endpoint that allows publishers to be viewed or edited."""

    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        # print(self.kwargs)

        try:
            obj = queryset.get(
                book_id=self.request.data.get("book"),
                user_id=self.request.data.get("user"),
            )
        except ObjectDoesNotExist:
            rating_pk = self.kwargs.get("pk", None)
            if rating_pk:
                obj = queryset.get(pk=rating_pk)
            else:
                obj = None

        self.check_object_permissions(self.request, obj)
        return obj

    def create(self, request, *args, **kwargs):
        # print('request.data: {}'.format(request.data))
        book_id = request.data.get("book")
        user_id = request.data.get("user")
        rating = None
        try:
            rating = Rating.objects.get(book_id=book_id, user_id=user_id)
            # print('rating: {}'.format(rating))
        except ObjectDoesNotExist:
            pass

        if not rating:
            return super(RatingViewSet, self).create(request, *args, **kwargs)
        else:
            return super(RatingViewSet, self).update(request, *args, **kwargs)

    def perform_destroy(self, instance):
        rating_id = instance.id
        try:
            rating = Rating.objects.get(id=rating_id)
            book_id = rating.book.id
            book = Book.objects.get(id=book_id)
        except ObjectDoesNotExist:
            book_id = None
            book = None
        instance.delete()

        if book and book_id:
            rating_average = (
                Rating.objects.filter(book_id=book_id)
                .aggregate(Avg("rating"))
                .get("rating__avg")
            )
            if rating_average:
                book.average_rating = round(rating_average, 1)
            else:
                book.average_rating = 0
            book.save()
