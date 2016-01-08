from django.contrib import admin
from django import forms
from django.forms.formsets import formset_factory

from blog.models import Post, Author, Category, ImageSingle, Typo, SubscribeEmail

import PIL
from PIL import Image
import string
import datetime
import random
import os


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

    def save_model(self, request, obj, form, change):

        def get_upload_path():
            date_path = datetime.datetime.now()
            token = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(16))

            return os.path.join('thumbs', str(date_path.year), str(date_path.month), str(date_path.day), str(date_path.hour), token + '.jpg')

        if form.is_valid():
            if not obj.id_post:
                post = Post.objects.all().order_by('-id_post').first()
                obj.id_post = post.id_post + 1

            super(PostAdmin, self).save_model(request, obj, form, change)

            image_new = Image.open(obj.image)
            (width, height) = image_new.size

            maxWidth = 400;             # Max width for the image
            maxHeight = 400;            # Max height for the image
            ratio = 0;                  # Used for aspect ratio

            # Check if the current width is larger than the max
            if width > maxWidth:
                ratio = maxWidth / width   # get ratio for scaling image
                size = (maxWidth, height * ratio)

            elif height > maxHeight:                 # Check if current height is larger than max
                ratio = maxHeight / height           # get ratio for scaling image
                size = (width * ratio, maxHeight)

            size = (int(size[0]), int(size[1]))

            new_path = obj.image.path.replace('/images/', '/thumbs/')

            # image_new = image_new.resize(size, Image.ANTIALIAS)
            # obj.image_thumbnail = image_new

            # image_thumb_new = obj.image_thumbnail
            obj.image_thumbnail = image_new.resize(size, Image.ANTIALIAS)

            image_thumb_new = image_new.resize(size, Image.ANTIALIAS)
            # image_thumb_new.save("/home/misha/Projects/Press/media/" + get_upload_path(), "JPEG")

            #size_test = 128, 128
            #im = Image.open(obj.image)
            #im.thumbnail(size_test)
            #im.save("/home/misha/Projects/Press/media/thumbs/2015/12/25/11/ffff.jpg" + ".thumbnail", "JPEG")


            # obj.image_thumbnail.save(new_path)

            # obj.save()

            """
            size = ( int(size[0]), int(size[1]) )
            image_new = image_new.resize(size, Image.ANTIALIAS)
            # image_new.save(obj.image.path)
            obj.save()
            """


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
