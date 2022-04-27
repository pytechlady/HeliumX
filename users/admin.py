from django.contrib import admin
from .models import Session, Subcription, Ticket, User


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','username', 'email', 'phone_number', 'user_type', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('username', 'email', 'phone_number')
    
admin.site.register(User,UserAdmin)


class SubcriptionAdmin(admin.ModelAdmin):
    list_display = ('id','subscription_type', 'created_at', 'updated_at')
    list_filter = ('subscription_type',)
    search_fields = ('subscription_type',)
    
admin.site.register(Subcription, SubcriptionAdmin)


class SessionAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'description', 'session_date', 'is_done')
    list_filter = ('session_date', 'is_done')
    search_fields = ('title', 'description')
    
admin.site.register(Session, SessionAdmin)


class TicketAdmin(admin.ModelAdmin):
    list_display = ('id','ticket_title', 'ticket_description', 'is_resolved')
    list_filter = ('ticket_title','is_resolved')
    search_fields = ('ticket_title', 'is_resolved')
    
admin.site.register(Ticket, TicketAdmin)
