# -*- coding: utf-8 -*-
from rest_framework import renderers
from www.util import camelize


class CamelCaseJSONRenderer(renderers.JSONRenderer):
    def render(self, data, *args, **kwargs):
        return super(CamelCaseJSONRenderer, self).render(
            camelize(data), *args, **kwargs
        )
