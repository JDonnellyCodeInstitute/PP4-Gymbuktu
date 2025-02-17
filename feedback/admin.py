from django.contrib import admin
from .models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'timestamp', 'content')
    search_fields = ('user__username', 'content')
    list_filter = ('timestamp',)
