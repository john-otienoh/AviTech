from django.contrib import admin
from .models import Post, Comment, Profile

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Customizing Display of models"""
    list_display = ['title', 'slug', 'author', 'publish', 'status']
    list_filter = ['status', 'created', 'publish', 'author']
    search_fields = ['title', 'body'] 
    prepopulated_fields = {'slug':('title',)} 
    raw_id_fields = ['author'] 
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']
    show_facets = admin.ShowFacets.ALWAYS

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Customizing Display of models"""
    list_display = ['name', 'post', 'active', 'commented']
    list_filter = ['active', 'commented']
    search_fields = ['name', 'body']
    show_facets = admin.ShowFacets.ALWAYS

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    "Customize User Profile in The Admin panel "
    list_display = ['user', 'photo']
    raw_id_fields = ['user']
