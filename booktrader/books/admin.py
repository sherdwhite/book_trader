from django.contrib import admin

from .models import Author, Book, BookCondition, Publisher, Rating


class AuthorInline(admin.TabularInline):
    model = Book.authors.through
    extra = 1


class RatingInline(admin.TabularInline):
    model = Rating
    extra = 0
    readonly_fields = ["created_at", "updated_at"]


class BookConditionInline(admin.TabularInline):
    model = BookCondition
    extra = 0
    readonly_fields = ["created_at", "updated_at"]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "author_names",
        "publisher",
        "genre",
        "average_rating",
        "isbn",
    ]
    list_filter = ["genre", "publication_date", "publisher", "language"]
    search_fields = ["title", "isbn", "authors__name", "publisher__name"]
    readonly_fields = ["average_rating", "created_at", "updated_at"]
    filter_horizontal = ["authors"]
    inlines = [RatingInline, BookConditionInline]

    fieldsets = (
        ("Basic Info", {"fields": ("title", "authors", "publisher", "description")}),
        (
            "Publication Details",
            {"fields": ("isbn", "publication_date", "page_count", "language", "genre")},
        ),
        ("Market Info", {"fields": ("original_price", "average_rating")}),
        ("Media", {"fields": ("cover_image",)}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["name", "birth_date", "created_at"]
    search_fields = ["name", "bio"]
    readonly_fields = ["created_at"]


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ["name", "founded_year", "created_at"]
    search_fields = ["name"]
    readonly_fields = ["created_at"]


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ["book", "user", "rating", "created_at"]
    list_filter = ["rating", "created_at"]
    search_fields = ["book__title", "user__username", "review"]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(BookCondition)
class BookConditionAdmin(admin.ModelAdmin):
    list_display = [
        "book",
        "owner",
        "condition",
        "is_available_for_trade",
        "is_available_for_auction",
    ]
    list_filter = ["condition", "is_available_for_trade", "is_available_for_auction"]
    search_fields = ["book__title", "owner__username"]
    readonly_fields = ["created_at", "updated_at"]
