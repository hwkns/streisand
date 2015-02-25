# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import UserProfile, UserAnnounceKey, UserIPAddress, UserAnnounce


class UserProfileAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'invited_by_link',
    )

    readonly_fields = (
        'user',
        'invited_by_link',
        'last_seeded',
    )

    exclude = (
        'invited_by',
    )

    def get_queryset(self, request):
        queryset = super(UserProfileAdmin, self).get_queryset(request)
        return queryset.select_related('user')

    def has_delete_permission(self, request, obj=None):
        return False

    def invited_by_link(self, profile):
        if profile.invited_by is not None:
            return profile.invited_by.admin_link
    invited_by_link.allow_tags = True
    invited_by_link.short_description = "Invited by"


class UserAnnounceKeyAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'profile_link',
        'used_since',
    )

    fields = (
        'id',
        'profile_link',
        'used_since',
    )

    readonly_fields = fields

    search_fields = (
        'id',
        'used_with_profile__user__username',
    )

    ordering = ['-used_since']

    def profile_link(self, announce_key):
        return announce_key.used_with_profile.admin_link
    profile_link.allow_tags = True


class UserIPAddressAdmin(admin.ModelAdmin):

    list_display = (
        'ip_address',
        'profile_link',
        'used_with',
        'first_used',
        'last_used',
    )

    fields = (
        'ip_address',
        'profile_link',
        'used_with',
    )

    readonly_fields = fields

    search_fields = (
        'ip_address',
        'profile__user__username',
    )

    def profile_link(self, user_ip_address):
        return user_ip_address.profile.admin_link
    profile_link.allow_tags = True


class UserAnnounceAdmin(admin.ModelAdmin):

    list_display = (
        'time_stamp',
        'announce_key',
        'swarm',
        'ip_address',
        'port',
        'peer_id',
        'new_bytes_uploaded',
        'new_bytes_downloaded',
        'bytes_remaining',
        'event',
    )

    ordering = ['-time_stamp']


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserAnnounceKey, UserAnnounceKeyAdmin)
admin.site.register(UserIPAddress, UserIPAddressAdmin)
admin.site.register(UserAnnounce, UserAnnounceAdmin)
