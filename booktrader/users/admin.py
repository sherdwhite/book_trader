from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import UserProfile, UserReputation


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = "Profile"


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "reputation_score", "is_verified", "created_at"]
    list_filter = ["is_verified", "willing_to_ship_internationally", "country"]
    search_fields = ["user__username", "user__email", "city", "state"]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(UserReputation)
class UserReputationAdmin(admin.ModelAdmin):
    list_display = ["user", "reputation_type", "points", "created_at"]
    list_filter = ["reputation_type", "created_at"]
    search_fields = ["user__username", "description"]
    readonly_fields = ["created_at"]
