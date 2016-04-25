# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import GuildStaff


class UserDetailView(LoginRequiredMixin, DetailView):
    model = GuildStaff
    # These next two lines tell the view to index lookups by email
    slug_field = 'email'
    slug_url_kwarg = 'email'


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse('users:detail',
                       kwargs={'email': self.request.user.email})


class UserUpdateView(LoginRequiredMixin, UpdateView):

    fields = ['name', ]

    model = GuildStaff

    # send the staffers back to their own page after a successful update
    def get_success_url(self):
        return reverse('users:detail',
                       kwargs={'email': self.request.user.email})

    def get_object(self):
        # Only get the GuildStaff record for the staffer making the request
        return GuildStaff.objects.get(email=self.request.user.email)


class UserListView(LoginRequiredMixin, ListView):
    model = GuildStaff
    # These next two lines tell the view to index lookups by email
    slug_field = 'email'
    slug_url_kwarg = 'email'
