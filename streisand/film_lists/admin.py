# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import FilmList, FilmListItem


class FilmInline(admin.TabularInline):
    model = FilmListItem
    extra = 0
    raw_id_fields = (
        'film',
    )
    autocomplete_lookup_fields = {
        'fk': ['film'],
    }


class FilmListAdmin(admin.ModelAdmin):

    fields = (
        'title',
        'description',
    )

    list_display = (
        'title',
    )

    search_fields = (
        'title',
    )

    inlines = (
        FilmInline,
    )


admin.site.register(FilmList, FilmListAdmin)
