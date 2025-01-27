from django.contrib import admin
from .models import Class, Booking

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'instructor', 'start_time', 'end_time', 'facility', 'capacity')
    search_fields = ('name', 'instructor', 'facility__name')
    list_filter = ('start_time', 'facility')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'gym_class', 'status', 'date')
    list_filter = ('status', 'date')
    search_fields = ('user__username', 'gym_class__name')
