from django.contrib import admin
from .models import Post, Tag

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'post_type', 'is_published', 'created_at']
    list_filter = ['post_type', 'is_published', 'tags']
    search_fields = ['title', 'content']

class TagAdmin(admin.ModelAdmin):
    search_fields = ['name']

admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)

