from django.contrib import admin

from .models import User, Zone


class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "role", 'zone']
    list_editable = ["role", "zone"]


admin.site.register(User, UserAdmin)
admin.site.register(Zone)
