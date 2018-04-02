# -*- coding: utf-8 -*-

from rest_framework import serializers

from django.contrib.auth.models import Group

from .models import User


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class AdminUserProfileSerializer(serializers.ModelSerializer):

    user_class = serializers.StringRelatedField()

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'url',
            'account_status',
            'user_class',
            'groups',
            'is_donor',
            'custom_title',
            'avatar_url',
            'profile_description',
            'average_seeding_size',
            'staff_notes',
            'irc_key',
            'invite_count',
            'bytes_uploaded',
            'bytes_downloaded',
            'last_seeded',
        )


class OwnedUserProfileSerializer(AdminUserProfileSerializer):
    username = serializers.StringRelatedField()

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
            'profile_description',
            'average_seeding_size',
            'irc_key',
            'invite_count',
            'bytes_uploaded',
            'bytes_downloaded',
            'last_seeded',
        )

        extra_kwargs = {'username': {'read_only': True, 'required': True}}


class PublicUserProfileSerializer(OwnedUserProfileSerializer):
    username = serializers.StringRelatedField()

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
            'profile_description',
            'average_seeding_size',
            'bytes_uploaded',
            'bytes_downloaded',
            'last_seeded',
        )

    extra_kwargs = {'username': {'read_only': True, 'required': True}}


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
