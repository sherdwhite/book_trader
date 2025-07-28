# encoding: utf-8

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Trade(models.Model):
    """Book trade between two users"""

    # Participants
    initiator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="trades_initiated",
        help_text="User who started the trade",
    )
    responder = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="trades_responded",
        help_text="User responding to the trade",
    )

    # Trade Details
    title = models.CharField(max_length=255, help_text="Trade description")
    description = models.TextField(
        blank=True, help_text="Additional trade details or notes"
    )

    # Status
    STATUS_CHOICES = [
        ("proposed", "Proposed"),
        ("counter_offered", "Counter Offered"),
        ("accepted", "Accepted"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
        ("disputed", "Disputed"),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="proposed")

    # Shipping & Money
    initiator_pays_shipping = models.BooleanField(
        default=True, help_text="Does initiator pay their own shipping?"
    )
    responder_pays_shipping = models.BooleanField(
        default=True, help_text="Does responder pay their own shipping?"
    )
    cash_difference = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0.00,
        help_text=(
            "Cash amount (+ means initiator pays responder, "
            "- means responder pays initiator)"
        ),
    )

    # Timestamps
    proposed_at = models.DateTimeField(auto_now_add=True)
    accepted_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    # Expiration
    expires_at = models.DateTimeField(
        blank=True, null=True, help_text="When this trade offer expires"
    )

    class Meta:
        ordering = ["-proposed_at"]

    def __str__(self):
        return f"Trade: {self.initiator.username} <-> {self.responder.username}"

    @property
    def is_expired(self):
        """Check if trade offer has expired"""
        return (
            self.expires_at
            and timezone.now() > self.expires_at
            and self.status == "proposed"
        )

    @property
    def can_be_accepted(self):
        """Check if trade can be accepted"""
        return self.status in ["proposed", "counter_offered"] and not self.is_expired


class TradeItem(models.Model):
    """Books being offered in a trade"""

    trade = models.ForeignKey(Trade, on_delete=models.CASCADE, related_name="items")
    book = models.ForeignKey("books.Book", on_delete=models.CASCADE)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, help_text="Who owns this book"
    )

    # Book condition and details
    CONDITION_CHOICES = [
        ("new", "New"),
        ("like_new", "Like New"),
        ("very_good", "Very Good"),
        ("good", "Good"),
        ("acceptable", "Acceptable"),
        ("poor", "Poor"),
    ]
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    condition_notes = models.TextField(blank=True)
    estimated_value = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Estimated value of this book",
    )

    # Images
    image1 = models.ImageField(upload_to="trade_images/", blank=True)
    image2 = models.ImageField(upload_to="trade_images/", blank=True)

    class Meta:
        unique_together = ["trade", "book", "owner"]

    def __str__(self):
        condition_display = self.get_condition_display()  # type: ignore
        return f"{self.book.title} ({self.owner.username}) - {condition_display}"


class TradeMessage(models.Model):
    """Messages between users during trade negotiation"""

    trade = models.ForeignKey(Trade, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_system_message = models.BooleanField(
        default=False, help_text="True for automated system messages"
    )

    class Meta:
        ordering = ["timestamp"]

    def __str__(self):
        return f"Message from {self.sender.username} in trade {self.trade.id}"


class TradeOffer(models.Model):
    """Track different versions of trade offers (for counter-offers)"""

    trade = models.ForeignKey(Trade, on_delete=models.CASCADE, related_name="offers")
    offered_by = models.ForeignKey(User, on_delete=models.CASCADE)

    # This would link to TradeItems for this specific offer version
    description = models.TextField(help_text="Description of this offer")
    cash_difference = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Offer by {self.offered_by.username} for trade {self.trade.id}"
