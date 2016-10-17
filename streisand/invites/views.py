# -*- coding: utf-8 -*-

import logging

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import permission_required
from django.http import Http404
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import View

from www.forms import RegistrationForm

from .models import Invite
from .forms import InviteForm


class InviteView(View):

    invites = []

    def dispatch(self, request, *args, **kwargs):
        self.invites = Invite.objects.filter(offered_by=request.user.profile)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):

        invite_form = InviteForm(offered_by=request.user.profile)
        return self._render(invite_form)

    @method_decorator(permission_required('profiles.can_invite', raise_exception=True))
    def post(self, request):

        invite_form = InviteForm(
            request.POST,
            offered_by=request.user.profile,
        )
        if invite_form.is_valid():
            new_invite = invite_form.save()
            new_invite.send_email()
            invite_form = InviteForm(offered_by=request.user.profile)
            return self._render(invite_form)

        # Render the form with errors
        return self._render(invite_form)

    def _render(self, form):
        """
        Render the page with the given form.
        """
        return render(
            request=self.request,
            template_name='invite_index.html',
            context={
                'invites': self.invites,
                'form': form,
            },
        )


class InviteRegistrationView(View):

    template_name = 'register.html'
    form = RegistrationForm()
    invite_key = None

    def dispatch(self, request, *args, **kwargs):

        # Allow valid invite keys; everything else is a 404
        self.invite_key = kwargs.pop('invite_key')
        if not Invite.objects.is_valid(self.invite_key):
            raise Http404

        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return self.render_form()

    def post(self, request):

        self.form = RegistrationForm(request.POST)

        if self.form.is_valid():

            # Flag potential dupers
            if request.user.is_authenticated:
                log = logging.getLogger('streisand.security')
                log.warning(
                    'New user "{new_user}" registered while logged in as '
                    'existing user "{existing_user}".'.format(
                        new_user=self.form.cleaned_data['username'],
                        existing_user=request.user.username,
                    )
                )

            invite = Invite.objects.get(key=self.invite_key)
            offered_by = invite.offered_by
            invite.delete()
            new_user = self.form.save()
            new_user.profile.invited_by = offered_by
            new_user.profile.save()

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
            context={'form': self.form},
        )
