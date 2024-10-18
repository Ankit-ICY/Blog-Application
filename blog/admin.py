# blog/admin.py
from django.contrib import admin
from .models import Blog, Comment, Tag

class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ['title', 'author', 'created_at']

admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment)
admin.site.register(Tag)
