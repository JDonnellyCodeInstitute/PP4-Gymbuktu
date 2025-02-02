from django.contrib import admin
from .models import Class, Booking, Instructor

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'instructor', 'start_time', 'end_time', 'facility')
    search_fields = ('name', 'instructor', 'facility__name')
    list_filter = ('start_time', 'facility')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'gym_class', 'class_status', 'date')
    list_filter = ('class_status', 'date')
    search_fields = ('user__username', 'gym_class__name')
