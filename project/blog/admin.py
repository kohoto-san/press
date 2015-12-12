from django.contrib import admin
from django import forms
from django.forms.formsets import formset_factory

from blog.models import Post, Author, Category, Image


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Post, PostAdmin)


admin.site.register(Author)
admin.site.register(Category)

""""
class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']


class PersonAdmin(admin.ModelAdmin):
    exclude = ['age']
    form = PersonForm

class ImageInline(admin.StackedInline):
    model = Image
    # extra = 3
    ImageFormSet = formset_factory(ImageForm)
"""
