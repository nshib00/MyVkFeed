from django.contrib import admin

from .models import *

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'date')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'text')
    list_filter = ('title',)


admin.site.register(Post, PostAdmin)