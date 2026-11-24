from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Post, Opportunity, Report, Appeal

@admin.register(User)
class NetworkUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (("Professional profile", {"fields": ("headline", "location", "is_verified_professional")}),)
    list_display = ("username", "email", "is_active", "is_staff", "is_verified_professional")

admin.site.register(Post)
admin.site.register(Opportunity)
admin.site.register(Report)
admin.site.register(Appeal)
