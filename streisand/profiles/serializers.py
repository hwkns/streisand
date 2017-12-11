# -*- coding: utf-8 -*-

from rest_framework import serializers

from .models import UserProfile


class AdminUserProfileSerializer(serializers.ModelSerializer):

    user_class = serializers.CharField(source='user_class.name')

    class Meta:
        model = UserProfile
        fields = (
            'id',
            'username',
            'email',
            'user_class',
            'account_status',
            'is_donor',
            'custom_title',
            'avatar_url',
            'description',
            'average_seeding_size',
            'staff_notes',
            'irc_key',
            'invite_count',
            'bytes_uploaded',
            'bytes_downloaded',
            'last_seeded',
        )


class OwnedUserProfileSerializer(AdminUserProfileSerializer):

    class Meta(AdminUserProfileSerializer.Meta):
        fields = (
            'id',
            'username',
            'email',
            'user_class',
            'account_status',
            'is_donor',
            'custom_title',
            'avatar_url',
            'description',
            'average_seeding_size',
            'irc_key',
            'invite_count',
            'bytes_uploaded',
            'bytes_downloaded',
            'last_seeded',
        )


class PublicUserProfileSerializer(OwnedUserProfileSerializer):

    class Meta(OwnedUserProfileSerializer.Meta):
        fields = (
            'id',
            'username',
            'email',
            'user_class',
            'account_status',
            'is_donor',
            'custom_title',
            'avatar_url',
            'description',
            'average_seeding_size',
            'bytes_uploaded',
            'bytes_downloaded',
            'last_seeded',
        )


class DisplayUserProfileSerializer(PublicUserProfileSerializer):

    class Meta(PublicUserProfileSerializer.Meta):
        fields = (
            'id',
            'username',
            'user_class',
            'account_status',
            'is_donor',
            'custom_title',
            'avatar_url',
        )
