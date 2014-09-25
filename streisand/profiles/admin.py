# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import UserProfile, UserAuthKey, UserIPAddress, UserAnnounce


class UserProfileAdmin(admin.ModelAdmin):

    list_display = (
        'user',
    )

    def get_queryset(self, request):
        queryset = super(UserProfileAdmin, self).get_queryset(request)
        return queryset.select_related('user')


class UserAuthKeyAdmin(admin.ModelAdmin):

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

    def profile_link(self, user_auth_key):
        return '<a href="{profile_url}">{username}</a>'.format(
            profile_url=user_auth_key.used_with_profile.get_absolute_url(),
            username=user_auth_key.used_with_profile.username,
        )
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
        return '<a href="{profile_url}">{username}</a>'.format(
            profile_url=user_ip_address.profile.get_absolute_url(),
            username=user_ip_address.profile.username,
        )
    profile_link.allow_tags = True


class UserAnnounceAdmin(admin.ModelAdmin):

    list_display = (
        'time_stamp',
        'auth_key',
        'info_hash',
        'ip_address',
        'port',
        'peer_id',
        'new_bytes_uploaded',
        'new_bytes_downloaded',
        'bytes_remaining',
        'event',
    )


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserAuthKey, UserAuthKeyAdmin)
admin.site.register(UserIPAddress, UserIPAddressAdmin)
admin.site.register(UserAnnounce, UserAnnounceAdmin)
