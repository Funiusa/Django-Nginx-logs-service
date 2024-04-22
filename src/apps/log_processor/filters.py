from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class IPAddressLengthFilter(admin.SimpleListFilter):
    title = _("IP address length")
    parameter_name = "ip_length"

    def lookups(self, request, model_admin):
        return (
            ("ipv4", _("IPv4 Addresses")),
            ("ipv6", _("IPv6 Addresses")),
        )

    def queryset(self, request, queryset):
        if self.value() == "ipv4":
            return queryset.filter(ip_address__regex=r"^(\d{1,3}\.){3}\d{1,3}$")
        if self.value() == "ipv6":
            return queryset.filter(
                ip_address__regex=r"^([\da-fA-F]{0,4}\:){7}[\da-fA-F]{0,4}$"
            )


class IPTypeFilter(admin.SimpleListFilter):
    title = _("IP Type")
    parameter_name = "ip_type"

    def lookups(self, request, model_admin):
        return (
            ("ipv4", _("IPv4")),
            ("ipv6", _("IPv6")),
        )

    def queryset(self, request, queryset):
        if self.value() == "ipv4":
            return queryset.filter(ip_address__regex=r"^(\d{1,3}\.){3}\d{1,3}$")
        if self.value() == "ipv6":
            return queryset.filter(
                ip_address__regex=r"^([\da-fA-F]{0,4}\:){7}[\da-fA-F]{0,4}$"
            )
