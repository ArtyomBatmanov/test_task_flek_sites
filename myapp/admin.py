from django.contrib import admin
from .models import User, Organization

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'phone', 'is_active', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    filter_horizontal = ('organizations',)  # Позволяет выбрать организации через фильтры

class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

admin.site.register(User, UserAdmin)
admin.site.register(Organization, OrganizationAdmin)
