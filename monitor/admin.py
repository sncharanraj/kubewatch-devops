from django.contrib import admin
from .models import URL, CheckResult


@admin.register(URL)
class URLAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "created_at")
    search_fields = ("name", "address")


@admin.register(CheckResult)
class CheckResultAdmin(admin.ModelAdmin):
    list_display = ("url", "status_code", "is_up", "response_time_ms", "checked_at")
    list_filter = ("is_up", "status_code", "checked_at")
    search_fields = ("url__name", "url__address")
