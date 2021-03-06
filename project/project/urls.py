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

from blog import views
from hunt.views import redirect
from spectest import urls as spectest_urls
from quiz import urls as quiz_urls
from hunt import urls as hunt_urls

from django.conf import settings
from django.conf.urls.static import static

from os import environ

# from project.feeds import LatestEntriesFeed
# from django.utils.feedgenerator import published_feeds
# from django.utils.feedgenerator import LatestEntriesFeed


urlpatterns = [

    url(r'^redirect/', redirect, name='redirect'),

    url(r'^accounts/', include('allauth.urls')),
    url(r'^admin/', admin.site.urls),

    # url(r'^$', PostList.as_view(), name='home'),
    # url(r'^$', load_posts, name='home'),

    url(r'^$', views.load_home, name='home'),
    # url(r'^news/', views.load_news, name='news'),
    url(r'^articles/', views.load_articles, name='articles'),

    url(r'^links/', views.headline_list, name='headlines'),
    url(r'^l/(?P<slug>[\w-]+)/*$', views.link, name='link'),

    # url(r'^form/', views.email_create, name='email_create'),

    url(r'^p/(?P<slug>[\w-]+)/*$', views.PostDetail.as_view(), name='post_detail'),
    url(r'^typo/', views.typo_send, name='typo_send'),

    # url(r'^contacts/', views.contactPage, name='contacts'),
    url(r'^contact/', views.NewContactCreate.as_view(), name='contact'),

    url(r'^special/', include(spectest_urls)),
    url(r'^quiz/', include(quiz_urls)),
    url(r'^startups/', include(hunt_urls, namespace='hunt', app_name='hunt')),

    # url(r'^feed/$', views.LatestEntriesFeed()),
    # url(r'^feeds/$', 'django.contrib.syndication.views.Feed', {'feed_dict': published_feeds}, 'view_name'),

]

urlpatterns += patterns(
    '',
    url(r'^feed/', views.LatestEntriesFeed()),
    # url(r'^feed/$', views.LatestEntriesFeed()),
)

if environ['DEBUG_BOOL']:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
