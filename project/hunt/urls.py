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
from hunt import views

urlpatterns = [

    # url(r'^$', views.PostList.as_view(), name='post_list'),
    url(r'^$', views.post_list, name='post_list'),
    url(r'^load-posts', views.load_posts, name='load_posts'),

    # url(r'^new/', views.PostCreate.as_view(), name='post_create'),

    url(r'^(?P<slug>[\w-]+)/$', views.PostDetail.as_view(), name='post_detail'),
    url(r'^profile/(?P<pk>\d+)/$', views.ProfileDetails.as_view(), name='profile_details'),
    url(r'^vote/(?P<post_id>\d+)/$', views.vote, name='vote'),
]
