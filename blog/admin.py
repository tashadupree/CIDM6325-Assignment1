from django.contrib import admin
from .models import Comment, Post, Recipe

# Register your models here.

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status']
    list_filter = ['status', 'created', 'publish', 'author']
    search_fields = ['title', 'body',]
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']
    show_facets = admin.ShowFacets.ALWAYS

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'instructions', 'servings')
    list_filter = ['created', 'publish', 'author']
    search_fields = ['title', 'body', 'ingredients']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['publish', 'title'] 

@admin.action(description='Mark selected comments as active')

def make_active(self, request, queryset):
    queryset.update(active=True)
    
make_active.short_description = "Mark selected comments as active"

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    actions = [make_active]
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']



    
