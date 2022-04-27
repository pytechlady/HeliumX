from django.contrib import admin
from .models import Session, Subcription, Ticket, User

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('id','username', 'email', 'phone_number', 'user_type', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('username', 'email', 'phone_number')
    
admin.site.register(User,UserAdmin)
admin.site.register(Subcription)
admin.site.register(Session)
admin.site.register(Ticket)
