# -*- coding: utf-8 -*-

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import permission_required
from django.db import transaction
from django.http import Http404
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import View

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .serializers import InviteSerializer

from www.forms import RegistrationForm
from www.views import RegistrationView

from .models import Invite
from .forms import InviteForm


class InviteViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = InviteSerializer
    queryset = Invite.objects.all(

    ).prefetch_related(
        'offered_by',
    ).order_by(
        'created_at'
    )

    def perform_create(self, serializer):
        serializer.validated_data['offered_by'] = self.request.user
        return super(InviteViewSet, self).perform_create(serializer)


class InviteView(View):

    invites = []

    def dispatch(self, request, *args, **kwargs):
        self.invites = Invite.objects.filter(offered_by=request.user)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):

        invite_form = InviteForm(offered_by=request.user)
        return self._render(invite_form)

    @method_decorator(permission_required('users.can_invite', raise_exception=True))
    def post(self, request):

        invite_form = InviteForm(
            request.POST,
            offered_by=request.user,
        )
        if invite_form.is_valid():
            new_invite = invite_form.save()
            new_invite.send_email()
            invite_form = InviteForm(offered_by=request.user)
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


class InviteRegistrationView(RegistrationView):

    invite_key = None

    def dispatch(self, request, *args, **kwargs):

        # Allow valid invite keys; everything else is a 404
        self.invite_key = kwargs.pop('invite_key')
        if not Invite.objects.is_valid(self.invite_key):
            raise Http404

        return super().dispatch(request, *args, **kwargs)

    def post(self, request):

        form = RegistrationForm(request.POST)

        if form.is_valid():

            self.log_potential_dupers(request, form)

            invite = Invite.objects.get(key=self.invite_key)
            offered_by = invite.offered_by

            # Consume the invite and create the new user
            with transaction.atomic:
                invite.delete()
                new_user = form.save()
                new_user.invited_by = offered_by
                new_user.save()

            # Authenticate the newly registered user
            new_authenticated_user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
            )
            login(request, new_authenticated_user)
            return redirect('home')

        else:

            return self.render_form(form)
