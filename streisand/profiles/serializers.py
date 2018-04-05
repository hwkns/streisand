# -*- coding: utf-8 -*-

from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import UserProfile


class AdminUserProfileSerializer(ModelSerializer):

    user_class = SerializerMethodField()

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

    def get_user_class(self, profile):
        return profile.user_class.name


class OwnedUserProfileSerializer(AdminUserProfileSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        remove_fields = (
            'staff_notes',
        )
        for field_name in remove_fields:
            self.fields.pop(field_name)


class PublicUserProfileSerializer(ModelSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        remove_fields = (
            'irc_key',
            'invite_count',

        )
        for field_name in remove_fields:
            self.fields.pop(field_name)
