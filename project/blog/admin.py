from django.contrib import admin
from django import forms
from django.forms.formsets import formset_factory

from blog.models import Post, Author, Category, Typo, SubscribeEmail, Media, Headline, ExternalLink, NewContact, ImageSingle

import PIL
from PIL import Image
import string
import datetime
import random
import os


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

    def save_model(self, request, obj, form, change):

        if form.is_valid():
            if not obj.id_post:
                post = Post.objects.all().order_by('-id_post').first()
                obj.id_post = post.id_post + 1

            super(PostAdmin, self).save_model(request, obj, form, change)

admin.site.register(Post, PostAdmin)


admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Typo)
admin.site.register(SubscribeEmail)

admin.site.register(Media)
admin.site.register(Headline)
admin.site.register(ExternalLink)

admin.site.register(NewContact)
admin.site.register(ImageSingle)


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
