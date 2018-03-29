# -*- coding: utf-8 -*-

from rest_framework.renderers import JSONRenderer


# http://stackoverflow.com/a/19053800
def to_camel_case(snake_str):
    components = snake_str.split('_')
    # We capitalize the first letter of each component except the first one
    # with the 'title' method and join them together.
    return components[0] + "".join(x.title() for x in components[1:])


def camel_case_data(data):

    if isinstance(data, list):
        return [camel_case_data(each) for each in data]

    if isinstance(data, dict):
        return {to_camel_case(key): camel_case_data(value) for key, value in data.items()}

    return data


class CamelCaseJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        data = camel_case_data(data)

        return super(CamelCaseJSONRenderer, self).render(
            data=data,
            accepted_media_type=accepted_media_type,
            renderer_context=renderer_context
        )
