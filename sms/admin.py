from django.contrib import admin

from sms.models import Number

class NumberAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'user', 'active', 'blacklist')


admin.site.register(Number, NumberAdmin)