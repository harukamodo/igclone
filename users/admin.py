from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import Profile
from users.forms import UserRegistrationForm, UserUpdateForm

# Register your models here.

class UserAdmin(BaseUserAdmin):
    form = UserUpdateForm
    add_form = UserRegistrationForm

    list_display = ('username', 'first_name', 'last_name', 'email', 'bio')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('password',)}),
        ('Personal info',
            {'fields': ('first_name','last_name','email',)
            }),
        ('Public info',
            {'fields': ('username', 'bio',)
            })
    )
    add_field_sets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username','first_name', 'last_name', 'email', 'bio',
                'password1', 'password2')}
        )
    )
    search_fields = ('username',)
    ordering = ('add_date',)
    filter_horizontal = ()

admin.site.register(Profile, UserAdmin)
admin.site.unregister(Group)
