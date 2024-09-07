from django.contrib import admin

from account.models import Interest, Account

admin.site.register([Interest, Account])