from django.contrib import admin
from .models import Category, Thread, Post

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'creator', 'created_at', 'slug')
    list_filter = ('category', 'creator')
    search_fields = ('title', 'creator__username')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-created_at',)
    raw_id_fields = ('creator',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'thread', 'author', 'created_at')
    list_filter = ('thread__category', 'author')
    search_fields = ('content', 'author__username', 'thread__title')
    ordering = ('-created_at',)
    raw_id_fields = ('author',)
