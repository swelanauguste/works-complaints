from django.contrib import admin

from .models import User, Zone


class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "zone"]
    list_editable = ["zone"]
    search_fields = ["username"]


admin.site.register(User, UserAdmin)
admin.site.register(Zone)
