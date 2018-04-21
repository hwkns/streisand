# -*- coding: utf-8 -*-

import logging


from django.contrib.auth import authenticate, login as auth_login
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic import View

from www.models import Feature

from .forms import RegistrationForm


def home(request):

    return render(
        request=request,
        template_name='index.html',
    )


class RegistrationView(View):

    def dispatch(self, request, *args, **kwargs):

        if not Feature.objects.is_enabled('open_registration'):
            raise Http404

        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return self.render_form(RegistrationForm())

    def post(self, request):

        form = RegistrationForm(request.POST)

        if form.is_valid():

            # Flag potential dupers
            self.log_potential_dupers(request, form)

            form.save()

            # Authenticate the newly registered user
            new_authenticated_user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
            )
            auth_login(request, new_authenticated_user)
            return redirect('home')

        else:

            return self.render_form(form)

    @staticmethod
    def log_potential_dupers(request, form):

        if request.user.is_authenticated:
            log = logging.getLogger('streisand.security')
            log.warning(
                'New user "{new_user}" registered while logged in as '
                'existing user "{existing_user}".'.format(
                    new_user=form.cleaned_data['username'],
                    existing_user=request.user.username,
                )
            )

    def render_form(self, form):
        return render(
            request=self.request,
            template_name='register.html',
            context={'form': form},
        )
