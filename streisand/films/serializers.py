# -*- coding: utf-8 -*-

from rest_framework import serializers

from .models import Film


class AdminFilmSerializer(serializers.ModelSerializer):

    imdb_id = serializers.SerializerMethodField()

    class Meta:
        model = Film
        fields = (
            'id',
            'title',
            'year',
            'imdb_id',
            'tmdb_id',
            'poster_url',
            'fanart_url',
            'trailer_url',
            'trailer_type',
            'duration_in_minutes',
            'description',
            'moderation_notes',
            'tags',
        )

    def get_imdb_id(self, film):
        if film.imdb:
            return film.imdb.tt_id


class PublicFilmSerializer(AdminFilmSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        remove_fields = (
            'moderation_notes',
        )
        for field_name in remove_fields:
            self.fields.pop(field_name)
