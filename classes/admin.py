from django.contrib import admin
from .models import Class

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'instructor', 'start_time', 'end_time', 'facility', 'capacity')
    search_fields = ('name', 'instructor', 'facility__name')
    list_filter = ('start_time', 'facility')
