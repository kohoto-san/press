from django.db import models
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount

from allauth.account.signals import user_signed_up, user_logged_in
from django.dispatch import receiver

from django.utils import timezone

import os
import datetime
import string
import random


@receiver(user_logged_in, dispatch_uid="some.unique.string.id.for.allauth.user_signed_up")
def user_logged_in_(request, user, **kwargs):
    from hunt.utils import createProfile

    social_account = SocialAccount.objects.filter(user_id=user.id).first()

    createProfile(social_account, user)


class Profile(models.Model):

    user = models.OneToOneField(User, primary_key=True)
    id_profile = models.IntegerField(blank=True)

    def get_upload_path(instance, filename):
        return os.path.join('avatars', str(instance.user.id) + filename[-4:])

    avatar = models.ImageField(upload_to=get_upload_path, default="default.png")

    ACTIVE = 'active'
    NO_ACTIVE = 'no_active'

    TYPE_PROFILE_CHOICES = (
        (ACTIVE, 'Active'),
        (NO_ACTIVE, 'No Active'),
    )
    type_profile = models.CharField(max_length=20,
                                    choices=TYPE_PROFILE_CHOICES,
                                    default=NO_ACTIVE)

    """
    def save(self, *args, **kwargs):

        if 'form' in kwargs:
            form = kwargs['form']
        else:
            form = None

        if self.pk is None:
            try:
                profile = Profile.objects.all().order_by('-id_profile').first().id_profile
            except AttributeError:
                profile = 0
            self.id_profile = profile + 1

        super(Profile, self).save(*args, **kwargs)
    """

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self):
        return self.user.username


def id_generator(size=32, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    id_str = ''.join(random.choice(chars) for i in range(size))

    while(Invite.objects.filter(text=id_str)):
        id_str = ''.join(random.choice(chars) for i in range(size))

    return id_str


class Invite(models.Model):

    profile = models.ForeignKey(Profile, blank=True, null=True)
    text = models.CharField(max_length=32, blank=True)

    def save(self, *args, **kwargs):

        if self.pk is None:
            self.text = id_generator()

        return super(Invite, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Invite"
        verbose_name_plural = "Invites"

    def __str__(self):
        return self.text


class Post(models.Model):

    slug = models.SlugField(unique=True, max_length=80)

    title = models.CharField(max_length=50, verbose_name='Название')
    description = models.CharField(max_length=100, verbose_name='Описание')
    author = models.ForeignKey(Profile, blank=True)

    link = models.URLField(verbose_name='Ссылка на сайт')

    upvotes = models.ManyToManyField(Profile, related_name='post_upvotes', blank=True)
    makers = models.ManyToManyField(Profile, related_name='post_makers', blank=True)

    upvotes_count = models.IntegerField(default=1)

    time_create = models.DateTimeField(default=timezone.now)
    date_create = models.DateField(default=timezone.now)

    def save(self, *args, **kwargs):

        try:
            self.upvotes_count = self.upvotes.count()
        except ValueError:
            self.upvotes_count = 1

        return super(Post, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return self.title


class Comment(models.Model):

    profile = models.ForeignKey(Profile)
    text = models.TextField()

    post = models.ForeignKey(Post)
    # parent_comment = models.ForeignKey(Comment)

    time_create = models.DateTimeField(default=timezone.now)
    date_create = models.DateField(default=timezone.now)

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __str__(self):
        return self.text
