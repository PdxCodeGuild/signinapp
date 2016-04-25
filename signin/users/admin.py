# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext_lazy as _

from .models import GuildStaff


class GuildStaffCreationForm(forms.ModelForm):
    """
    A form for creating new Guild Staffers. Includes all the required
    fields, plus a repeated password.
    """
    error_messages = {
        'duplicate_email': _('This email has already been taken.'),
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = GuildStaff
        fields = (
            'email',
            'first_name',
            'last_name'
        )

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'])
        return password2

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            GuildStaff.objects.get(email=email)
        except GuildStaff.DoesNotExist:
            return email
        raise forms.ValidationError(self.error_messages['duplicate_email'])

    def save(self, commit=True):
        # Save the provided password in hashed format
        staffer = super(GuildStaffCreationForm, self).save(commit=False)
        staffer.set_password(self.cleaned_data["password1"])
        if commit:
            staffer.save()
        return staffer


class GuildStaffChangeForm(forms.ModelForm):
    """
    A form for updating Guild Staffers. Includes all the fields on the
    staffer, but replaces the password field with admin's password hash
    display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = GuildStaff
        fields = '__all__'

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


@admin.register(GuildStaff)
class UserAdmin(AuthUserAdmin):
    form = GuildStaffChangeForm
    add_form = GuildStaffCreationForm

    # The fields to be used in displaying the GuildStaff model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()
