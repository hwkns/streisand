# -*- coding: utf-8 -*-

import json
import logging

from django.contrib.auth import authenticate, login
from django.http import Http404
from django.views.generic import View
from django.shortcuts import render, redirect

from .forms import RegistrationForm
from .models import Feature


def home(request):
    return render(
        request=request,
        template_name='home.html',
        dictionary={
        }
    )


class RegistrationView(View):

    template_name = 'register.html'
    form = RegistrationForm()
    invite_key = None

    def dispatch(self, request, *args, **kwargs):

        if not Feature.objects.is_enabled('open_registration'):
            raise Http404

        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return self.render_form()

    def post(self, request):

        self.form = RegistrationForm(request.POST)

        if self.form.is_valid():

            # Flag potential dupers
            if request.user.is_authenticated():
                log = logging.getLogger('streisand.security')
                log.warning(
                    'New user "{new_user}" registered while logged in as '
                    'existing user "{existing_user}".'.format(
                        new_user=self.form.cleaned_data['username'],
                        existing_user=request.user.username,
                    )
                )

            self.form.save()

            # Authenticate the newly registered user
            new_authenticated_user = authenticate(
                username=self.form.cleaned_data['username'],
                password=self.form.cleaned_data['password1'],
            )
            login(request, new_authenticated_user)
            return redirect('home')

        else:

            return self.render_form()

    def render_form(self):
        return render(
            request=self.request,
            template_name=self.template_name,
            dictionary={'form': self.form},
        )


def template_viewer(request, template_path):
    return render(request, template_path, json.loads(request.GET.get('context', '{}')))
