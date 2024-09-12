from django.contrib import admin

from account.models import Account, Interest


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    search_fields = ("username", "phone")
    list_filter = ("is_staff", "is_superuser")


admin.site.register(
    [
        Interest,
    ]
)
