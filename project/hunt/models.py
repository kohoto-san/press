from django.db import models
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount

from allauth.account.signals import user_signed_up, user_logged_in
from django.dispatch import receiver

from django.utils import timezone

import os
import datetime


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

    avatar = models.ImageField(upload_to=get_upload_path)

    def save(self, *args, **kwargs):

        if 'form' in kwargs:
            form = kwargs['form']
        else:
            form = None

        if self.pk is None and form is not None and 'id_profile' in form.changed_data:
            profile = Profile.objects.all().order_by('-id_profile').first()
            if profile is None:
                profile = 0
            self.id_profile = profile.id_profile + 1

        super(Profile, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self):
        return self.user.username


class Post(models.Model):

    slug = models.SlugField(unique=True)

    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    author = models.ForeignKey(Profile, blank=True)

    link = models.URLField()

    upvotes = models.ManyToManyField(Profile, related_name='post_upvotes', blank=True)
    makers = models.ManyToManyField(Profile, related_name='post_makers', blank=True)

    time_create = models.DateTimeField(default=timezone.now)
    date_create = models.DateField(default=timezone.now)

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

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __str__(self):
        return self.text
