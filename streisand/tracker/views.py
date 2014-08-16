# -*- coding: utf-8 -*-

from django.views.generic import View
from django.http import HttpResponse


class AnnounceView(View):

    def get(self, request, auth_key):
        return HttpResponse(
            'Hello, world!\n\n'
            '{auth_key}\n\n'
            '{params}'.format(
                auth_key=auth_key,
                params=request.GET.dict(),
            )
        )
