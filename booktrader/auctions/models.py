# encoding: utf-8

from decimal import Decimal

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


class Auction(models.Model):
    """Book auction listing"""

    # Basic Info
    title = models.CharField(max_length=255, help_text="Auction title")
    description = models.TextField(
        help_text="Detailed description of the book and its condition"
    )
    book = models.ForeignKey(
        "books.Book", on_delete=models.CASCADE, related_name="auctions"
    )
    seller = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="auctions_selling"
    )

    # Book Condition
    CONDITION_CHOICES = [
        ("new", "New"),
        ("like_new", "Like New"),
        ("very_good", "Very Good"),
        ("good", "Good"),
        ("acceptable", "Acceptable"),
        ("poor", "Poor"),
    ]
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    condition_notes = models.TextField(
        blank=True, help_text="Additional notes about condition"
    )

    # Auction Details
    starting_price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))]
    )
    reserve_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Minimum price for sale (hidden from bidders)",
    )
    buy_now_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Price for immediate purchase",
    )

    # Timing
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField()

    # Status
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("active", "Active"),
        ("ended", "Ended"),
        ("sold", "Sold"),
        ("cancelled", "Cancelled"),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")

    # Shipping
    shipping_cost = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text="Shipping cost (0 for free shipping)",
    )
    ships_to_countries = models.TextField(
        default="US", help_text="Comma-separated country codes (e.g., US,CA,UK)"
    )

    # Images
    image1 = models.ImageField(upload_to="auction_images/", blank=True)
    image2 = models.ImageField(upload_to="auction_images/", blank=True)
    image3 = models.ImageField(upload_to="auction_images/", blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Auction: {self.title} by {self.seller.username}"

    @property
    def current_price(self):
        """Get current highest bid or starting price"""
        highest_bid = self.bids.order_by("-amount").first()  # type: ignore
        return highest_bid.amount if highest_bid else self.starting_price

    @property
    def is_active(self):
        """Check if auction is currently active"""
        now = timezone.now()
        return self.status == "active" and self.start_time <= now <= self.end_time

    @property
    def time_remaining(self):
        """Get time remaining in auction"""
        if self.status != "active":
            return None
        now = timezone.now()
        return self.end_time - now if self.end_time > now else None


class Bid(models.Model):
    """Bid placed on an auction"""

    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))]
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    is_auto_bid = models.BooleanField(
        default=False, help_text="True if this was placed by automatic bidding system"
    )
    max_bid_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Maximum amount for automatic bidding",
    )

    class Meta:
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["auction", "-amount"]),
        ]

    def __str__(self):
        return f"${self.amount} bid by {self.bidder.username} on {self.auction.title}"


class WatchList(models.Model):
    """Users can watch auctions they're interested in"""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="watched_auctions"
    )
    auction = models.ForeignKey(
        Auction, on_delete=models.CASCADE, related_name="watchers"
    )
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user", "auction"]

    def __str__(self):
        return f"{self.user.username} watching {self.auction.title}"
