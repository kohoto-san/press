from django.db import models
from django.utils.text import slugify

from ckeditor.fields import RichTextField

import random
import string
import datetime
import os

import PIL
from PIL import Image

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit


class ImageSingle(models.Model):

    def get_upload_path(instance, filename):
        date_path = datetime.datetime.now()
        token = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(16))

        return os.path.join('post-images', str(date_path.year), str(date_path.month), str(date_path.day), str(date_path.hour), token + filename[-6:])

    image = models.ImageField(upload_to=get_upload_path)

    class Meta:
        verbose_name = "ImageSingle"
        verbose_name_plural = "ImageSingles"

    def __str__(self):
        return self.image.url


class SubscribeEmail(models.Model):

    email = models.EmailField(max_length=254)

    class Meta:
        verbose_name = "SubscribeEmail"
        verbose_name_plural = "SubscribeEmails"

    def __str__(self):
        return self.email


class Author(models.Model):

    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"

    def __str__(self):
        return self.name


class Category(models.Model):

    text = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categorys"

    def __str__(self):
        return self.text


class Post(models.Model):

    id_post = models.IntegerField(blank=True, null=True)

    slug = models.SlugField()

    author = models.ForeignKey(Author)
    category = models.ForeignKey(Category)

    title = models.CharField(max_length=255)

    text_entry = models.TextField()
    text = RichTextField()

    date = models.DateTimeField(auto_now_add=True)
    views_count = models.IntegerField(default=0)

    def get_upload_path(instance, filename):
        date_path = datetime.datetime.now()
        token = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(16))

        return os.path.join('images', str(date_path.year), str(date_path.month), str(date_path.day), str(date_path.hour), token + filename[-6:])

    image = models.ImageField(upload_to=get_upload_path)
    # image_thumbnail = models.ImageField(upload_to=get_upload_path, null=True, blank=True)

    image_thumbnail = ImageSpecField(source='image',
                                     processors=[ResizeToFit(width=450)],
                                     format='JPEG',
                                     options={'quality': 80})

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return self.title

"""
        "Max width and height 800"        
        if (800 / width < 800 / height):
            factor = 800.0 / height
        else:
            factor = 800.0 / width

        factor = int(factor)
        size = ( width / factor, height / factor)
        # size = (100, 100)
        
        image_new = image_new.resize(size, Image.ANTIALIAS)
        image_new.save(self.image.path)
"""


class Typo(models.Model):

    post = models.ForeignKey(Post)
    text = models.TextField()
    comment = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Typo"
        verbose_name_plural = "Typos"

    def __str__(self):
        return self.post.title + " ——— " + self.text


class Contact(models.Model):

    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    text = models.TextField()

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"

    def __str__(self):
        return self.text
