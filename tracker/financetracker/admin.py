from django.contrib import admin
from .models import *


class FinanceAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user', 'money', 'date', 'is_income']


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'grade', 'user', 'date']


admin.site.register(Finance, FinanceAdmin)
admin.site.register(Review, ReviewAdmin)

