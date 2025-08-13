# -*- coding: utf-8 -*-

from datetime import timedelta
from decimal import Decimal

import pytest
from books.models import Author, Book, Publisher
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from trades.models import Trade, TradeItem, TradeMessage, TradeOffer


class TestTradeModel(TestCase):
    def setUp(self):
        self.initiator = User.objects.create_user(
            username="initiator", email="initiator@example.com", password="testpass123"
        )
        self.responder = User.objects.create_user(
            username="responder", email="responder@example.com", password="testpass123"
        )

        self.trade = Trade.objects.create(
            initiator=self.initiator,
            responder=self.responder,
            title="Test Trade",
            description="A test trade",
            status="proposed",
            expires_at=timezone.now() + timedelta(days=7),
        )

    def test_trade_str(self):
        """Test trade string representation"""
        expected = f"Trade: {self.initiator.username} <-> {self.responder.username}"
        assert str(self.trade) == expected

    def test_is_expired_property_future(self):
        """Test is_expired property for future expiry"""
        # Future expiry should not be expired
        assert self.trade.is_expired is False

    def test_is_expired_property_past(self):
        """Test is_expired property for past expiry"""
        # Past expiry with proposed status should be expired
        self.trade.expires_at = timezone.now() - timedelta(days=1)
        self.trade.save()
        assert self.trade.is_expired is True

    def test_is_expired_property_non_proposed(self):
        """Test is_expired property for non-proposed status"""
        # Past expiry with non-proposed status should not be expired
        self.trade.expires_at = timezone.now() - timedelta(days=1)
        self.trade.status = "accepted"
        self.trade.save()
        assert self.trade.is_expired is False

    def test_is_expired_property_no_expiry(self):
        """Test is_expired property when no expiry is set"""
        self.trade.expires_at = None
        self.trade.save()
        assert self.trade.is_expired is False

    def test_can_be_accepted_property_proposed(self):
        """Test can_be_accepted property for proposed trade"""
        # Proposed trade with future expiry should be acceptable
        assert self.trade.can_be_accepted is True

    def test_can_be_accepted_property_counter_offered(self):
        """Test can_be_accepted property for counter-offered trade"""
        self.trade.status = "counter_offered"
        self.trade.save()
        assert self.trade.can_be_accepted is True

    def test_can_be_accepted_property_expired(self):
        """Test can_be_accepted property for expired trade"""
        self.trade.expires_at = timezone.now() - timedelta(days=1)
        self.trade.save()
        assert self.trade.can_be_accepted is False

    def test_can_be_accepted_property_completed(self):
        """Test can_be_accepted property for completed trade"""
        self.trade.status = "completed"
        self.trade.save()
        assert self.trade.can_be_accepted is False


class TestTradeItemModel(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            username="owner", email="owner@example.com", password="testpass123"
        )
        self.other_user = User.objects.create_user(
            username="other", email="other@example.com", password="testpass123"
        )

        self.author = Author.objects.create(name="Test Author")
        self.publisher = Publisher.objects.create(name="Test Publisher")
        self.book = Book.objects.create(
            title="Test Book", isbn="1234567890123", publisher=self.publisher
        )
        self.book.authors.add(self.author)

        self.trade = Trade.objects.create(
            initiator=self.owner,
            responder=self.other_user,
            title="Test Trade",
            description="A test trade",
        )

        self.trade_item = TradeItem.objects.create(
            trade=self.trade,
            book=self.book,
            owner=self.owner,
            condition="good",
            condition_notes="Well maintained",
            estimated_value=Decimal("15.00"),
        )

    def test_trade_item_str(self):
        """Test trade item string representation"""
        expected = f"{self.book.title} ({self.owner.username}) - Good"
        assert str(self.trade_item) == expected

    def test_unique_together_constraint(self):
        """Test that same book/owner can't be added to same trade twice"""
        with pytest.raises(Exception):  # Should raise IntegrityError
            TradeItem.objects.create(
                trade=self.trade, book=self.book, owner=self.owner, condition="new"
            )


class TestTradeMessageModel(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(
            username="sender", email="sender@example.com", password="testpass123"
        )
        self.receiver = User.objects.create_user(
            username="receiver", email="receiver@example.com", password="testpass123"
        )

        self.trade = Trade.objects.create(
            initiator=self.sender,
            responder=self.receiver,
            title="Test Trade",
            description="A test trade",
        )

        self.message = TradeMessage.objects.create(
            trade=self.trade,
            sender=self.sender,
            message="Hello, interested in this trade!",
            is_system_message=False,
        )

    def test_trade_message_str(self):
        """Test trade message string representation"""
        expected = f"Message from {self.sender.username} in trade {self.trade.pk}"
        assert str(self.message) == expected

    def test_system_message(self):
        """Test system message creation"""
        system_msg = TradeMessage.objects.create(
            trade=self.trade,
            sender=self.sender,
            message="Trade status updated to accepted",
            is_system_message=True,
        )
        assert system_msg.is_system_message is True

    def test_message_ordering(self):
        """Test messages are ordered by timestamp"""
        # Create another message
        msg2 = TradeMessage.objects.create(
            trade=self.trade, sender=self.receiver, message="Sure, let's discuss!"
        )

        # Messages should be ordered by timestamp (ascending)
        messages = list(TradeMessage.objects.filter(trade=self.trade))
        assert messages[0] == self.message  # First message
        assert messages[1] == msg2  # Second message


class TestTradeOfferModel(TestCase):
    def setUp(self):
        self.offeror = User.objects.create_user(
            username="offeror", email="offeror@example.com", password="testpass123"
        )
        self.other_user = User.objects.create_user(
            username="other", email="other@example.com", password="testpass123"
        )

        self.trade = Trade.objects.create(
            initiator=self.offeror,
            responder=self.other_user,
            title="Test Trade",
            description="A test trade",
        )

        self.offer = TradeOffer.objects.create(
            trade=self.trade,
            offered_by=self.offeror,
            description="Initial offer: my book for your book",
            cash_difference=Decimal("5.00"),
            is_active=True,
        )

    def test_trade_offer_str(self):
        """Test trade offer string representation"""
        expected = f"Offer by {self.offeror.username} for trade {self.trade.pk}"
        assert str(self.offer) == expected

    def test_offer_ordering(self):
        """Test offers are ordered by creation time descending"""
        # Create another offer
        offer2 = TradeOffer.objects.create(
            trade=self.trade,
            offered_by=self.other_user,
            description="Counter offer",
            cash_difference=Decimal("0.00"),
        )

        # Most recent offer should be first
        offers = list(TradeOffer.objects.filter(trade=self.trade))
        assert offers[0] == offer2
        assert offers[1] == self.offer
