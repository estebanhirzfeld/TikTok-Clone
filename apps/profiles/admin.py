from django.contrib import admin
from .models import Profile, FollowRequest

class ProfileAdmin(admin.ModelAdmin):
    list_display = ["pkid", "id", "user", "gender", "is_private"]
    list_display_links = ["pkid", "id", "user"]
    list_filter = ["id", "pkid"]

class FollowRequestAdmin(admin.ModelAdmin):
    list_display = ["id", 'requester', 'target', 'created_at', 'accepted']
    list_filter = ['accepted',]
    search_fields = ('requester__user__first_name', 'requester__user__last_name', 'target__user__first_name', 'target__user__last_name')

admin.site.register(FollowRequest, FollowRequestAdmin)
admin.site.register(Profile, ProfileAdmin)