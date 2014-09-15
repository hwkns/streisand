# -*- coding: utf-8 -*-

from django.shortcuts import render

from tracker.models import Swarm


def home(request):
    return render(
        request=request,
        template_name='home.html',
        dictionary={
            'swarms': Swarm.objects.all(),
        }
    )
