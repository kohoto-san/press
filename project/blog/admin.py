from django.contrib import admin

from blog.models import Post, Author, Category


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Post, PostAdmin)


admin.site.register(Author)
admin.site.register(Category)
