"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include, patterns
from django.contrib import admin

from blog.views import PostList, PostDetail, load_posts, LatestEntriesFeed

from django.conf import settings
from django.conf.urls.static import static

# from project.feeds import LatestEntriesFeed
# from django.utils.feedgenerator import published_feeds
# from django.utils.feedgenerator import LatestEntriesFeed


urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # url(r'^$', PostList.as_view(), name='home'),

    url(r'^$', load_posts, name='home'),

    url(r'^p/(?P<slug>[\w-]+)/*$', PostDetail.as_view(), name='post_detail'),

    # url(r'^feed/$', LatestEntriesFeed()),
    # url(r'^feeds/$', 'django.contrib.syndication.views.Feed', {'feed_dict': published_feeds}, 'view_name'),

] # + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += patterns(
    '',
    url(r'^feed/', LatestEntriesFeed()),
    # url(r'^feed/$', LatestEntriesFeed()),
)
