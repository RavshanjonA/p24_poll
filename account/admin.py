from django.contrib import admin
from django.contrib.admin import TabularInline
from django.contrib.auth.models import Permission

from account.models import Account, Interest, AccountProfile


class AccountInfoTabularInline(TabularInline):
    model = AccountProfile
    extra = 1


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    APP_LABELS = {"account", "poll"}

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.filter(content_type__app_label__in=self.APP_LABELS)
        return queryset


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    inlines = (AccountInfoTabularInline,)
    search_fields = ("username", "phone")
    list_filter = ("is_staff", "is_superuser")


admin.site.register(
    [
        Interest,
    ]
)
