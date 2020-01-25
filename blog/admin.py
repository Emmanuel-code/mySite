from django.contrib import admin
from .models import Post
from .models import Comment
from tinymce.widgets import TinyMCE
from django.db import models

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug',	'author',	'publish','status')
    list_filter	= ('status',	'created',	'publish',	'author')
    search_fields =('title',	'body')
    prepopulated_fields	= {'slug':('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status',	'publish')

    formfield_overrides = {models.TextField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 30})},}

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post','created','active')
    list_filter = ('active','created', 'updated')
    search_fields = ('body',)