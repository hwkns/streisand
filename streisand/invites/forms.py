# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Invite


class InviteForm(forms.ModelForm):

    class Meta:
        model = Invite
        fields = (
            'email',
        )

    def __init__(self, *args, **kwargs):
        offered_by = kwargs.pop('offered_by')
        super(InviteForm, self).__init__(*args, **kwargs)
        self.instance.offered_by = offered_by

    def clean_email(self):
        # TODO: normalize email by lowercasing, removing dots and +extra
        email = self.cleaned_data['email']
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("There is already a user with that email address.")
        else:
            return email
