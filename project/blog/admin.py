from django.contrib import admin
from django import forms
from django.forms.formsets import formset_factory

from blog.models import Post, Author, Category, ImageSingle, Typo, SubscribeEmail

import PIL
from PIL import Image


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

    def save_model(self, request, obj, form, change):
        if form.is_valid():
            if not obj.id_post:
                post = Post.objects.all().order_by('-id_post').first()
                obj.id_post = post.id_post + 1

            super(PostAdmin, self).save_model(request, obj, form, change)

            image_new = Image.open(obj.image)
            (width, height) = image_new.size

            maxWidth = 10;             # Max width for the image
            maxHeight = 10;            # Max height for the image
            ratio = 0;                  # Used for aspect ratio

            # Check if the current width is larger than the max
            if width > maxWidth:
                ratio = maxWidth / width   # get ratio for scaling image
                size = ( maxWidth, height * ratio )

            elif height > maxHeight:                 # Check if current height is larger than max
                ratio = maxHeight / height           # get ratio for scaling image
                size = ( width * ratio, maxHeight )

            size = ( int(size[0]), int(size[1]) )
            image_new = image_new.resize(size, Image.ANTIALIAS)
            # image_new.save(obj.image.path)
            obj.save()


admin.site.register(Post, PostAdmin)


admin.site.register(Author)
admin.site.register(Category)
admin.site.register(ImageSingle)
admin.site.register(Typo)
admin.site.register(SubscribeEmail)




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
