from django.contrib import admin
from .models import Organization, User, UserManager

admin.site.register(User)
admin.site.register(Organization)

# Register your models here.
