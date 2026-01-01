from django.contrib import admin
from .models import DailyActivity, ScheduleItem

# Register the Daily Activity Log
@admin.register(DailyActivity)
class DailyActivityAdmin(admin.ModelAdmin):
    list_display = ('child', 'activity_type', 'title', 'time', 'date')
    list_filter = ('activity_type', 'date')
    search_fields = ('child__full_name', 'title')

# Register the Class Schedule
@admin.register(ScheduleItem)
class ScheduleItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'group', 'start_time', 'color_theme')
    list_filter = ('group',)
    ordering = ('start_time',)