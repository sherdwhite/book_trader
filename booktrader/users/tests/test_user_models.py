# -*- coding: utf-8 -*-

from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from users.models import UserProfile, UserReputation


class TestUserProfileModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

        self.profile = UserProfile.objects.create(
            user=self.user,
            phone_number="+1234567890",
            address_line1="123 Main St",
            address_line2="Apt 4B",
            city="Test City",
            state="TS",
            postal_code="12345",
            country="US",
            is_verified=True,
        )

    def test_user_profile_str(self):
        """Test user profile string representation"""
        expected = f"{self.user.username}'s Profile"
        assert str(self.profile) == expected

    def test_full_address_property(self):
        """Test full_address property"""
        # The actual implementation only includes non-empty parts
        expected = "123 Main St, Apt 4B, Test City, TS, 12345"
        assert self.profile.full_address == expected

    def test_full_address_property_minimal(self):
        """Test full_address property with minimal data"""
        minimal_profile = UserProfile.objects.create(
            user=User.objects.create_user(
                username="minimal", email="minimal@example.com", password="testpass123"
            ),
            city="City",
            state="ST",
            country="US",
        )

        expected = "City, ST"  # Country not included in full_address
        assert minimal_profile.full_address == expected

    def test_full_address_property_with_postal_code(self):
        """Test full_address property with postal code but no address lines"""
        profile = UserProfile.objects.create(
            user=User.objects.create_user(
                username="test2", email="test2@example.com", password="testpass123"
            ),
            city="City",
            state="ST",
            postal_code="54321",
            country="US",
        )

        expected = "City, ST, 54321"  # Country not included in full_address
        assert profile.full_address == expected


class TestUserReputationModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="repuser", email="rep@example.com", password="testpass123"
        )

        self.reputation = UserReputation.objects.create(
            user=self.user,
            reputation_type="positive_feedback",
            points=Decimal("1.5"),
            description="Great seller, fast shipping!",
        )

    def test_user_reputation_str(self):
        """Test user reputation string representation"""
        expected = f"{self.user.username}: Positive Feedback (+1.5)"
        assert str(self.reputation) == expected

    def test_reputation_ordering(self):
        """Test reputation events are ordered by creation time descending"""
        # Create another reputation event
        rep2 = UserReputation.objects.create(
            user=self.user,
            reputation_type="trade_complete",
            points=Decimal("2.0"),
            description="Completed trade successfully",
        )

        # Most recent reputation should be first
        reps = list(UserReputation.objects.filter(user=self.user))
        assert reps[0] == rep2
        assert reps[1] == self.reputation

    def test_reputation_points_validation(self):
        """Test reputation points are within valid range"""
        # Valid points should work
        valid_rep = UserReputation.objects.create(
            user=self.user,
            reputation_type="account_penalty",
            points=Decimal("-2.0"),
            description="Penalty for violation",
        )
        assert valid_rep.points == Decimal("-2.0")

    def test_reputation_types(self):
        """Test all reputation types can be created"""
        reputation_types = [
            "auction_complete",
            "trade_complete",
            "positive_feedback",
            "negative_feedback",
            "verified_email",
            "verified_phone",
            "account_penalty",
        ]

        for rep_type in reputation_types:
            rep = UserReputation.objects.create(
                user=self.user,
                reputation_type=rep_type,
                points=Decimal("1.0"),
                description=f"Test {rep_type}",
            )
            assert rep.reputation_type == rep_type
