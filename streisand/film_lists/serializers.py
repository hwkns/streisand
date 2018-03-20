# -*- coding: utf-8 -*-

from rest_framework import serializers

from films.serializers import PublicFilmSerializer
from .admin import FilmList


class FilmListSerializer(serializers.ModelSerializer):

    collection_id = serializers.SerializerMethodField(source='pk')
    films = PublicFilmSerializer(read_only=True, many=True)

    class Meta:
        model = FilmList
        fields = ('collection_id', 'title', 'description', 'films')

    @staticmethod
    def get_collection_id(self):
        return self.id
