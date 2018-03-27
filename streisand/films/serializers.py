# -*- coding: utf-8 -*-

from rest_framework import serializers

from .models import Film, Collection, CollectionComment, FilmComment


class FilmCommentSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(default=serializers.CurrentUserDefault(), read_only=True)
    author_username = serializers.StringRelatedField(source='author', default=serializers.CurrentUserDefault(),
                                                     read_only=True)

    class Meta:
        model = FilmComment
        fields = (
            'film',
            'author',
            'author_username',
            'text',
            'created_at',
            'modified_at'
        )


class CollectionCommentSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(default=serializers.CurrentUserDefault(), read_only=True)
    author_username = serializers.StringRelatedField(source='author', default=serializers.CurrentUserDefault(),
                                                     read_only=True)

    class Meta:
        model = CollectionComment
        fields = (
            'collection',
            'author',
            'author_username',
            'text',
            'created_at',
            'modified_at'
        )


class AdminFilmSerializer(serializers.ModelSerializer):
    film_comments = FilmCommentSerializer(read_only=True, many=True, source='comments')
    imdb_id = serializers.SerializerMethodField()

    class Meta(FilmCommentSerializer.Meta):
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
            'film_comments',
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


class CollectionSerializer(serializers.ModelSerializer):
    creator_id = serializers.PrimaryKeyRelatedField(default=serializers.CurrentUserDefault(), read_only=True, source='creator')
    creator_username = serializers.StringRelatedField(default=serializers.CurrentUserDefault(), read_only=True, source='creator')
    list_id = serializers.IntegerField(source='id', read_only=True)
    list_title = serializers.CharField(source='title')
    list_description = serializers.CharField(source='description')
    film = serializers.PrimaryKeyRelatedField(many=True, queryset=Film.objects.all())
    film_title = serializers.StringRelatedField(many=True, read_only=True, source='film')
    film_link = serializers.HyperlinkedRelatedField(many=True, read_only=True, source='film', view_name='film-detail')
    url = serializers.HyperlinkedIdentityField(read_only=True, view_name='collection-detail')
    collection_comments = CollectionCommentSerializer(source='collections_comments', many=True, read_only=True)

    class Meta(CollectionCommentSerializer.Meta):
        model = Collection
        fields = (
            'creator_id',
            'creator_username',
            'collection_comments',
            'list_id',
            'url',
            'list_title',
            'list_description',
            'collection_tags',
            'film',
            'film_title',
            'film_link'
        )
