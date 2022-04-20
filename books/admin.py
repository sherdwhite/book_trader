# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Author, Book, Publisher, Rating

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Publisher)
admin.site.register(Rating)
