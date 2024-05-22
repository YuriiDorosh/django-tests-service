from django.contrib import admin

from apps.tests.models import Test


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "type", "created_at"]
    list_filter = ["type"]
    search_fields = ["name", "description"]
    readonly_fields = ["created_at"]
    fieldsets = ((None, {"fields": ("name", "description", "type", "created_at")}),)
    ordering = ["-created_at"]
    date_hierarchy = "created_at"
