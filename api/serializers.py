from django.contrib.auth.models import User
# from django.db.models import Avg
from rest_framework import serializers

from books.models import Book, Publisher, Author, Rating


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "pk",
            "username",
            "email",
            "groups",
        )


class BookSerializer(serializers.ModelSerializer):
    # average_rating = serializers.SerializerMethodField()
    #
    # @staticmethod
    # def get_average_rating(obj):
    #     rating_average = Rating.objects.filter(book_id=obj.id).aggregate(Avg('rating')).get('rating__avg')
    #     if rating_average:
    #         return round(rating_average, 1)
    #     else:
    #         return 0

    class Meta:
        model = Book
        fields = (
            "pk",
            "title",
            "description",
            "isbn",
            "authors",
            "publisher",
            "average_rating",
        )


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = (
            "pk",
            "name",
        )


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = (
            "pk",
            "name",
        )


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = (
            "pk",
            "rating",
            "user",
            "book",
        )
