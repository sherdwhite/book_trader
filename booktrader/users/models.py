# encoding: utf-8

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class UserProfile(models.Model):
    """Extended user profile for book trading/auction site"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    # Contact & Location
    phone_number = models.CharField(max_length=20, blank=True)
    address_line1 = models.CharField(max_length=255, blank=True)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True, default="US")

    # Profile Info
    bio = models.TextField(
        blank=True, help_text="Tell others about your reading interests"
    )
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    # Trading Preferences
    preferred_genres = models.TextField(
        blank=True, help_text="Comma-separated list of favorite genres"
    )
    willing_to_ship_internationally = models.BooleanField(default=False)
    max_shipping_distance_miles = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Maximum distance willing to ship (leave blank for no limit)",
    )

    # Reputation & Trust
    reputation_score = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=5.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        help_text="User reputation based on trading/auction history",
    )

    # Account Settings
    email_notifications = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False, help_text="Email/phone verified")

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return f"{self.user.username}'s Profile"

    @property
    def full_address(self):
        """Return formatted address"""
        parts = [
            self.address_line1,
            self.address_line2,
            self.city,
            self.state,
            self.postal_code,
        ]
        return ", ".join([part for part in parts if part])


class UserReputation(models.Model):
    """Track individual reputation events"""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reputation_events"
    )

    REPUTATION_TYPES = [
        ("auction_complete", "Completed Auction"),
        ("trade_complete", "Completed Trade"),
        ("positive_feedback", "Positive Feedback"),
        ("negative_feedback", "Negative Feedback"),
        ("verified_email", "Email Verified"),
        ("verified_phone", "Phone Verified"),
        ("account_penalty", "Account Penalty"),
    ]

    reputation_type = models.CharField(max_length=20, choices=REPUTATION_TYPES)
    points = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(-5.0), MaxValueValidator(5.0)],
    )
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Link to related objects
    related_auction = models.ForeignKey(
        "auctions.Auction", blank=True, null=True, on_delete=models.SET_NULL
    )
    related_trade = models.ForeignKey(
        "trades.Trade", blank=True, null=True, on_delete=models.SET_NULL
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username}: {self.get_reputation_type_display()} ({self.points:+.1f})"
