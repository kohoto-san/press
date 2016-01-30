
from .models import Profile

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

# import urllib2
import urllib.request


def createProfile(social_account, user):

    extra_data = social_account.extra_data

    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = Profile()

    profile.user = user

    if social_account.provider == "twitter":
        avatar_url = extra_data['profile_image_url']

    if social_account.provider == "vk":
        avatar_url = extra_data['photo_big']

    if social_account.provider == "facebook":
        avatar_url = "http://graph.facebook.com/%s/picture?type=large" % extra_data['id']

    # profile.avatar = extra_data['photo_big']

    img_format = avatar_url[-4:]

    img_temp = NamedTemporaryFile(delete=True)
    img_temp.write(urllib.request.urlopen(avatar_url).read())
    img_temp.flush()

    profile.avatar.save(str(profile.pk) + str(img_format), File(img_temp))

    profile.save()

    return profile
