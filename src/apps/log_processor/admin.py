from django.contrib import admin
from .models import NginxLogEntry
from .filters import IPTypeFilter, IPAddressLengthFilter


@admin.register(NginxLogEntry)
class NginxLogEntryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "ip_address",
        "date",
        "http_method",
        "request_uri",
        "response_code",
        "response_size",
    )
    list_filter = (
        IPTypeFilter,
        IPAddressLengthFilter,
        "http_method",
        "response_code",
        "date",
    )
    search_fields = ("ip_address", "request_uri")
    list_per_page = 30
