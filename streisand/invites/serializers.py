# -*- coding: utf-8 -*-

from rest_framework import serializers

from .models import Invite


class InviteSerializer(serializers.ModelSerializer):
    offered_by = serializers.PrimaryKeyRelatedField(default=serializers.CurrentUserDefault(), read_only=True)

    class Meta:
        model = Invite
        fields = ('offered_by', 'email', 'key', 'created_at', )
