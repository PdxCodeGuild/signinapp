# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.core.validators import RegexValidator
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


class GuildStaffManager(BaseUserManager):
    """
    Custom manager for GuildStaff.
    """
    use_in_migrations = True

    def _create_user(
        self,
        email,
        first_name,
        last_name,
        password,
        **extra_fields
    ):
        """
        Creates and saves a GuildStaffer with the given email, first_name,
        last_name and password.
        """
        if not email:
            raise ValueError('GuildStaffers must have an email address')

        if not first_name:
            raise ValueError('GuildStaffers must have a first name')

        if not last_name:
            raise ValueError('GuildStaffers must have a last name')

        staffer = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )

        staffer.set_password(password)
        staffer.save(using=self._db)
        return staffer

    def create_user(
        self,
        email,
        first_name,
        last_name,
        password=None,
        **extra_fields
    ):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(
            email,
            first_name,
            last_name,
            password,
            **extra_fields
        )

    def create_superuser(
        self,
        email,
        first_name,
        last_name,
        password,
        **extra_fields
    ):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(
            email,
            first_name,
            last_name,
            password,
            **extra_fields
        )


@python_2_unicode_compatible
class GuildStaff(AbstractBaseUser, PermissionsMixin):
    """
    A custom User model.

    This model represents all staff members, and is the basis of
    authentication and authorization for the signin app. Admins are
    staff members with unrestricted privileges.
    """
    # The email field is used as the unique identifier in GuildStaff.
    email = models.EmailField(
        _('email address'), max_length=255, unique=True)
    first_name = models.CharField(
        _('first name'), max_length=30)
    last_name = models.CharField(
        _('last name'), max_length=30)
    title = models.CharField(_('title of user'), blank=True, max_length=50)
    phone_regex = RegexValidator(
        regex=r'^(\d{3}) \d{3}-\d{4}$',
        message=_("Phone number format should follow: '(999) 999-9999'."),
    )
    phone = models.CharField(
        _('phone number'),
        validators=[phone_regex],
        max_length=14,
        blank=True,
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    objects = GuildStaffManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):
        # Returns the first_name and last_name for the guild staffer, with
        # a space in between.
        return "{} {}".format(self.first_name, self.last_name).strip()

    def get_short_name(self):
        # Returns the short name for the guild staffer
        return self.first_name

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    @property
    def is_staff(self):
        "Is the guild staffer an admin?"
        # Simplest possible answer: All admins are staff
        return self.is_staff

    class Meta:
        verbose_name = _('guild staffer')
        verbose_name_plural = _('guild staffers')
