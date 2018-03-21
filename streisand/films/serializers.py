# -*- coding: utf-8 -*-

from rest_framework import serializers

from .models import Film, Collection, CollectionComment

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
            'lists',
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


class FilmSerializer(serializers.ModelSerializer, serializers.PrimaryKeyRelatedField):
    class Meta:
        model = Film
        fields = ('id', 'lists', 'title', 'year', 'description', 'tags')


class CollectionSerializer(serializers.ModelSerializer):
    list_id = serializers.IntegerField(source='id', read_only=True)                                    
    list_title = serializers.CharField(source='title')                                                 
    list_description = serializers.CharField(source='description')
    film = serializers.PrimaryKeyRelatedField(many=True, queryset=Film.objects.all())
    url = serializers.HyperlinkedIdentityField(read_only=True, view_name='collection-detail')
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True, source='collections_comments')

    class Meta:
        model = Collection
        fields = ('creator', 'comments', 'list_id', 'url', 'list_title', 'list_description', 'collection_tags', 'film')
