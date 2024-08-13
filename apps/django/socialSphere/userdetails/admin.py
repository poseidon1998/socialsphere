from django.contrib import admin
from .models import SS_User, FriendRequest

class SS_UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'user_name', 'category', 'active_status', 'login_time')
    list_filter = ('active_status', 'category')
    search_fields = ('email', 'user_name')
    ordering = ('-id',)
    
    # def get_field_queryset(self, db, field_name, request):
    #     if field_name in ['groups', 'user_permissions']:
    #         return field_name.model.objects.filter(id=request.user.id)
    #     return super().get_field_queryset(db, field_name, request)

class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'created_at', 'status')
    list_filter = ('status', 'created_at')
    search_fields = ('from_user__email', 'to_user__email')
    ordering = ('-created_at',)

# Register the User model with the custom UserAdmin
admin.site.register(SS_User, SS_UserAdmin)

# Register the FriendRequest model
admin.site.register(FriendRequest, FriendRequestAdmin)
