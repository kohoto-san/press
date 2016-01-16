from django.db import models
from django.utils.text import slugify

from ckeditor.fields import RichTextField

import random
import string
import datetime
import os

from django.utils import timezone

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


def id_generator(size=8, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    slug = ''.join(random.choice(chars) for i in range(size))

    while(ExternalLink.objects.filter(internal=slug)):
        slug = ''.join(random.choice(chars) for i in range(size))

    return slug


class ExternalLink(models.Model):

    external = models.URLField()
    internal = models.CharField(max_length=50, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.internal = id_generator()

        return super(ExternalLink, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "ExternalLink"
        verbose_name_plural = "ExternalLinks"

    def __str__(self):
        return self.external


class Media(models.Model):

    name = models.CharField(max_length=100)
    link = models.URLField()

    class Meta:
        verbose_name = "Media"
        verbose_name_plural = "Medias"

    def __str__(self):
        return self.name


class HeadlineCycle(models.Model):

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "HeadlineCycle"
        verbose_name_plural = "HeadlineCycles"

    def __str__(self):
        return self.title


class Headline(models.Model):

    media = models.ForeignKey(Media)
    # cycle = models.ForeignKey(HeadlineCycle, blank=True, null=True)

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    link = models.URLField()
    smart_link = models.ForeignKey(ExternalLink, blank=True, null=True)

    date = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.smart_link = ExternalLink.objects.create(external=self.link)
        return super(Headline, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Headline"
        verbose_name_plural = "Headlines"

    def __str__(self):
        return self.title

"""
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.date = timezone.now()
        return super(Headline, self).save(*args, **kwargs)
"""


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


class NewContact(models.Model):

    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    text = models.TextField()

    class Meta:
        verbose_name = "NewContact"
        verbose_name_plural = "NewContacts"

    def __str__(self):
        return self.text
