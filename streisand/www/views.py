# -*- coding: utf-8 -*-

import json
import logging

from django.contrib.auth import authenticate, login
from django.http import Http404
from django.views.generic import View
from django.shortcuts import render, redirect

from invites.models import Invite

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

        # Allow valid invite keys
        if 'invite_key' in kwargs and Invite.objects.is_valid(kwargs['invite_key']):
            self.invite_key = kwargs.pop('invite_key')

        # Allow open registration with no invite key, when that feature is enabled
        elif 'invite_key' not in kwargs and Feature.objects.is_enabled('open_registration'):
            pass

        # Everything else is a 404
        else:
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

            new_user = self.form.save()

            if self.invite_key:
                invite = Invite.objects.get(key=self.invite_key)
                new_user.profile.invited_by = invite.owner
                new_user.profile.save()
                invite.delete()

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
