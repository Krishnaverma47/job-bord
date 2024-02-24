from django.contrib import admin
from user.models import User

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','email', 'first_name', 'last_name')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('email', 'first_name', 'last_name')

admin.site.register(User, UserAdmin)
