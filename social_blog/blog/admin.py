from django.contrib import admin

from .models import Post, Location, Category


# admin.site.register(Post)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass


# admin.site.register(Location)
@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    pass


# admin.site.register(Category)
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass
