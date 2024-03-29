from django.contrib import admin
from .models import Post, Comment, Category
from import_export.admin import ImportExportMixin

class PostAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug':('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')

admin.site.register(Post, PostAdmin)

class CommentAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('name','post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'body')

admin.site.register(Comment, CommentAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Category, CategoryAdmin)

    





# Register your models here.
