from django.contrib.auth.models import User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from typing import Set
from .forms import UserAdminCreationForm, UserAdminChangeForm
from django.contrib.auth import get_user_model
# Register your models here.
User = get_user_model()


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    list_display = ('email', 'admin',
                    'timestamp', 'active', 'staff')
    list_filter = ('admin', 'active', 'staff')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username',)}),
        ('Permissions', {
         'fields': ('admin', 'staff', )}),  # 'groups', 'user_permissions'
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
         ),
    )
    search_fields = ('email', 'username')
    ordering = ('email',)
    readonly_fields = ['timestamp']
    filter_horizontal = ()

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_admin
        print(form.base_fields)
        disabled_fields = set()  # type: Set[str]

        if not is_superuser:
            disabled_fields |= {
                'username',
                'admin',
                'email',
            }

        # Prevent non-superusers from editing their own permissions
        if (
            not is_superuser
            and obj is not None
            and obj == request.user
        ):
            disabled_fields |= {
                'staff',
                'admin',
                'email'
                # 'groups',
                # 'user_permissions',
            }

        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True

        return form


admin.site.register(User, UserAdmin)
