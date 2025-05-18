from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # Add fields you want to display in the admin interface
    list_display = ['username', 'email', 'first_name', 'last_name']
    search_fields = ['username', 'email']  # Required for autocomplete_fields