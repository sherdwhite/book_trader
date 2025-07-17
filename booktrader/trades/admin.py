from django.contrib import admin

from .models import Trade, TradeItem, TradeMessage, TradeOffer


class TradeItemInline(admin.TabularInline):
    model = TradeItem
    extra = 0


class TradeMessageInline(admin.TabularInline):
    model = TradeMessage
    extra = 0
    readonly_fields = ["timestamp"]


@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    list_display = ["id", "initiator", "responder", "status", "proposed_at"]
    list_filter = ["status", "proposed_at"]
    search_fields = ["initiator__username", "responder__username", "title"]
    readonly_fields = ["proposed_at", "accepted_at", "completed_at"]
    inlines = [TradeItemInline, TradeMessageInline]

    fieldsets = (
        ("Participants", {"fields": ("initiator", "responder")}),
        ("Trade Details", {"fields": ("title", "description", "status")}),
        (
            "Financial Terms",
            {
                "fields": (
                    "cash_difference",
                    "initiator_pays_shipping",
                    "responder_pays_shipping",
                )
            },
        ),
        (
            "Timeline",
            {"fields": ("proposed_at", "accepted_at", "completed_at", "expires_at")},
        ),
    )


@admin.register(TradeItem)
class TradeItemAdmin(admin.ModelAdmin):
    list_display = ["trade", "book", "owner", "condition", "estimated_value"]
    list_filter = ["condition", "owner"]
    search_fields = ["book__title", "owner__username"]


@admin.register(TradeMessage)
class TradeMessageAdmin(admin.ModelAdmin):
    list_display = ["trade", "sender", "timestamp", "is_system_message"]
    list_filter = ["is_system_message", "timestamp"]
    search_fields = ["trade__id", "sender__username", "message"]
    readonly_fields = ["timestamp"]


@admin.register(TradeOffer)
class TradeOfferAdmin(admin.ModelAdmin):
    list_display = ["trade", "offered_by", "cash_difference", "created_at", "is_active"]
    list_filter = ["is_active", "created_at"]
    search_fields = ["trade__id", "offered_by__username"]
    readonly_fields = ["created_at"]
