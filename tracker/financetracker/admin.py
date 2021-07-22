from django.contrib import admin
from .models import *


class FinanceAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user', 'money', 'date', 'is_income']


admin.site.register(Finance, FinanceAdmin)

