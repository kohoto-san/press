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

# from spectest import urls as spectest_urls
from quiz import views

# from spectest.models import Result
# from django.views.generic import DetailView

urlpatterns = [

    # url(r'^p/(?P<slug>[\w-]+)/*$', PostDetail.as_view(), name='post_detail'),
    # url(r'^typo/', typo_send, name='typo_send'),
    # url(r'^special/', include(spectest_urls))

    url(r'^$', views.home, name='home'),
    url(r'^save-answer/', views.save_answer, name='save_answer'),
    # url(r'^$', views.home, name='home'),

    url(r'^start/', views.startQuiz, name='start'),

    # url(r'^result/', views.result_calc, name='result_calc'),
    # url(r'^result/(?P<slug>[\w-]+)/*$', DetailView.as_view(model=Result))
]
