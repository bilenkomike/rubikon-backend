from django.contrib import admin
from .models import Contact

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "is_processed", "created_at")
    list_filter = ("is_processed",)
    search_fields = ("name", "email", "message")