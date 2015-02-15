# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import Codec, Container, Resolution, SourceMedia


admin.site.register(Codec)
admin.site.register(Container)
admin.site.register(Resolution)
admin.site.register(SourceMedia)
