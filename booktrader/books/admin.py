# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import Author, Book, Publisher, Rating

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Publisher)
admin.site.register(Rating)
