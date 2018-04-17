# -*- coding: utf-8 -*-

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.contrib.auth.models import Group
from invites.models import Invite

from users.models import User


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class AdminUserProfileSerializer(serializers.ModelSerializer):
    user_class_rank = serializers.PrimaryKeyRelatedField(source='user_class', read_only=True)
    user_class = serializers.StringRelatedField()

    class Meta:
        model = User
        fields = (
            'id',
            'user_class',
            'user_class_rank',
            'last_login',
            'username',
            'email',
            'is_superuser',
            'password',
            'is_staff',
            'is_active',
            'date_joined',
            'is_donor',
            'account_status',
            'failed_login_attempts',
            'avatar_url',
            'custom_title',
            'profile_description',
            'staff_notes',
            'irc_key',
            'invite_count',
            'bytes_uploaded',
            'bytes_downloaded',
            'last_seeded',
            'average_seeding_size',
            'announce_key',
            'invited_by',
            'watch_queue',
            'user_permissions',
            'torrents',
        )

        extra_kwargs = {'password': {'write_only': True, }}


class OwnedUserProfileSerializer(AdminUserProfileSerializer):
    salted_token_id_and_user = serializers.SerializerMethodField()

    class Meta:
        model = User(AdminUserProfileSerializer.Meta)
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
            'announce_key',
            'invite_count',
            'bytes_uploaded',
            'bytes_downloaded',
            'last_seeded',
            'salted_token_id_and_user',
        )

    extra_kwargs = {'username': {'read_only': True, 'required': True}}

    # String representation of the DRF Knox salted token and user name.

    @staticmethod
    def get_salted_token_id_and_user(user):
        return '%s' % (user.auth_token_set.last())


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


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(label='Email Address')

    invite_key = serializers.PrimaryKeyRelatedField(source='invited_by.key', queryset=Invite.objects.all())

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'email2',
            'password',
            'invite_key',

        ]
        extra_kwargs = {
            "password": {
                'write_only': True}
        }

    def validate(self, data):
        # email = data['email']
        # user_qs = User.objects.filter(email=email)
        # if user_qs.exists():
        #     raise ValidationError("This user has already registered.")
        return data

    def validate_email(self, value):
        data = self.get_initial()
        user_qs = User.objects.filter(email=value)
        if user_qs.exists():
            raise serializers.ValidationError("This email has already been used")

        return value

    def validate_invite_key(self, value):
        data = self.get_initial()
        self.invite_key = data.get("invite_key")
        if not Invite.objects.is_valid(self.invite_key):
            raise serializers.ValidationError("Invalid invite key")
        return value

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        user_obj = User(
            username=username,
            email=email
        )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    email = serializers.EmailField(label='Email Address')

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',

        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        # email = data['email']
        # user_qs = User.objects.filter(email=email)
        # if user_qs.exists():
        #     raise ValidationError("This user has already registered.")
        return data
