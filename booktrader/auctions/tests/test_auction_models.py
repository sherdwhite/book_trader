# -*- coding: utf-8 -*-

from datetime import timedelta
from decimal import Decimal

import pytest
from auctions.models import Auction, Bid, WatchList
from books.models import Author, Book, Publisher
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone


class TestAuctionModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="seller", email="seller@example.com", password="testpass123"
        )
        self.bidder = User.objects.create_user(
            username="bidder", email="bidder@example.com", password="testpass123"
        )
        self.author = Author.objects.create(name="Test Author")
        self.publisher = Publisher.objects.create(name="Test Publisher")
        self.book = Book.objects.create(
            title="Test Book", isbn="1234567890123", publisher=self.publisher
        )
        self.book.authors.add(self.author)

        self.auction = Auction.objects.create(
            title="Test Auction",
            description="A test auction",
            book=self.book,
            seller=self.user,
            condition="good",
            starting_price=Decimal("10.00"),
            end_time=timezone.now() + timedelta(days=7),
            status="active",
        )

    def test_current_price_no_bids(self):
        """Test current_price property when no bids exist"""
        assert self.auction.current_price == self.auction.starting_price

    def test_current_price_with_bids(self):
        """Test current_price property with bids"""
        # Create some bids
        Bid.objects.create(
            auction=self.auction, bidder=self.bidder, amount=Decimal("15.00")
        )
        Bid.objects.create(
            auction=self.auction, bidder=self.bidder, amount=Decimal("20.00")
        )

        # Should return highest bid amount
        assert self.auction.current_price == Decimal("20.00")

    def test_is_active_property(self):
        """Test is_active property"""
        # Active auction within time window
        assert self.auction.is_active is True

        # Inactive status
        self.auction.status = "ended"
        self.auction.save()
        assert self.auction.is_active is False

        # Expired auction
        self.auction.status = "active"
        self.auction.end_time = timezone.now() - timedelta(days=1)
        self.auction.save()
        assert self.auction.is_active is False

    def test_time_remaining_property(self):
        """Test time_remaining property"""
        # Active auction should have time remaining
        time_remaining = self.auction.time_remaining
        assert time_remaining is not None
        assert time_remaining.days > 0

        # Ended auction should return None
        self.auction.status = "ended"
        self.auction.save()
        assert self.auction.time_remaining is None

        # Expired auction should return None
        self.auction.status = "active"
        self.auction.end_time = timezone.now() - timedelta(days=1)
        self.auction.save()
        assert self.auction.time_remaining is None


class TestBidModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="seller", email="seller@example.com", password="testpass123"
        )
        self.bidder = User.objects.create_user(
            username="bidder", email="bidder@example.com", password="testpass123"
        )
        self.author = Author.objects.create(name="Test Author")
        self.publisher = Publisher.objects.create(name="Test Publisher")
        self.book = Book.objects.create(
            title="Test Book", isbn="1234567890123", publisher=self.publisher
        )
        self.auction = Auction.objects.create(
            title="Test Auction",
            description="A test auction",
            book=self.book,
            seller=self.user,
            condition="good",
            starting_price=Decimal("10.00"),
            end_time=timezone.now() + timedelta(days=7),
            status="active",
        )
        self.bid = Bid.objects.create(
            auction=self.auction, bidder=self.bidder, amount=Decimal("15.00")
        )

    def test_bid_ordering(self):
        """Test bids are ordered by timestamp descending"""
        # Create another bid
        bid2 = Bid.objects.create(
            auction=self.auction, bidder=self.bidder, amount=Decimal("20.00")
        )

        # Most recent bid should be first
        bids = list(Bid.objects.all())
        assert bids[0] == bid2
        assert bids[1] == self.bid


class TestWatchListModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="watcher", email="watcher@example.com", password="testpass123"
        )
        self.seller = User.objects.create_user(
            username="seller", email="seller@example.com", password="testpass123"
        )
        self.author = Author.objects.create(name="Test Author")
        self.publisher = Publisher.objects.create(name="Test Publisher")
        self.book = Book.objects.create(
            title="Test Book", isbn="1234567890123", publisher=self.publisher
        )
        self.auction = Auction.objects.create(
            title="Test Auction",
            description="A test auction",
            book=self.book,
            seller=self.seller,
            condition="good",
            starting_price=Decimal("10.00"),
            end_time=timezone.now() + timedelta(days=7),
            status="active",
        )
        self.watchlist = WatchList.objects.create(user=self.user, auction=self.auction)

    def test_unique_together_constraint(self):
        """Test that user can't watch same auction twice"""
        with pytest.raises(Exception):  # Should raise IntegrityError
            WatchList.objects.create(user=self.user, auction=self.auction)
