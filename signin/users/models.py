# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.core.validators import RegexValidator
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_('Name of User'), blank=True, max_length=50)
    title = models.CharField(_('Title'), blank=True, max_length=50)
    phone_regex = RegexValidator(
        regex=r'^(\d{3}) \d{3}-\d{4}$',
        message="Phone number format should follow: '(999) 999-9999'.")
    phone = models.CharField(
        validators=[phone_regex],
        max_length=14,
        blank=True)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})
