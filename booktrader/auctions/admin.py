from django.contrib import admin

from .models import Auction, Bid, WatchList


class BidInline(admin.TabularInline):
    model = Bid
    extra = 0
    readonly_fields = ["timestamp"]
    ordering = ["-amount"]


@admin.register(Auction)
class AuctionAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "seller",
        "starting_price",
        "current_price",
        "status",
        "end_time",
    ]
    list_filter = ["status", "condition", "created_at"]
    search_fields = ["title", "description", "seller__username", "book__title"]
    readonly_fields = ["created_at", "updated_at", "current_price"]
    inlines = [BidInline]

    fieldsets = (
        ("Basic Info", {"fields": ("title", "description", "book", "seller")}),
        ("Condition", {"fields": ("condition", "condition_notes")}),
        (
            "Pricing",
            {
                "fields": (
                    "starting_price",
                    "reserve_price",
                    "buy_now_price",
                    "current_price",
                )
            },
        ),
        ("Timing", {"fields": ("start_time", "end_time", "status")}),
        ("Shipping", {"fields": ("shipping_cost", "ships_to_countries")}),
        ("Images", {"fields": ("image1", "image2", "image3")}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ["auction", "bidder", "amount", "timestamp", "is_auto_bid"]
    list_filter = ["is_auto_bid", "timestamp"]
    search_fields = ["auction__title", "bidder__username"]
    readonly_fields = ["timestamp"]


@admin.register(WatchList)
class WatchListAdmin(admin.ModelAdmin):
    list_display = ["user", "auction", "added_at"]
    search_fields = ["user__username", "auction__title"]
    readonly_fields = ["added_at"]
