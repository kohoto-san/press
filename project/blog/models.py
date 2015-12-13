from django.db import models
from django.utils.text import slugify

from ckeditor.fields import RichTextField

import random
import string
import datetime
import os


class Image(models.Model):

    image = models.ImageField(upload_to="images/%Y/%m/%d/")

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"

    def __str__(self):
        pass
    


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
        
        return os.path.join('images', str(date_path.year), str(date_path.month), str(date_path.day), token + str(instance.id) + filename[-6:])


    image = models.ImageField(upload_to=get_upload_path)

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return self.title
