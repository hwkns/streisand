# -*- coding: utf-8 -*-
from rest_framework import parsers

from www.util import underscoreize

# From https://github.com/beda-software/djangorestframework-camel-case

class CamelCaseFormParser(parsers.FormParser):
    def parse(self, stream, media_type=None, parser_context=None):
        data = super(CamelCaseFormParser, self).parse(
            stream, media_type=media_type, parser_context=parser_context)
        return underscoreize(data)


class CamelCaseMultiPartParser(parsers.MultiPartParser):
    def parse(self, stream, media_type=None, parser_context=None):
        data_and_files = super(CamelCaseMultiPartParser, self).parse(
            stream, media_type=media_type, parser_context=parser_context)
        data_and_files.data = underscoreize(data_and_files.data)
        data_and_files.files = underscoreize(data_and_files.files)

        return data_and_files


class CamelCaseJSONParser(parsers.JSONParser):
    def parse(self, stream, media_type=None, parser_context=None):
        data = super(CamelCaseJSONParser, self).parse(
            stream, media_type=media_type, parser_context=parser_context)

        return underscoreize(data)
