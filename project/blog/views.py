from django.shortcuts import render, render_to_response

from django.views.generic import ListView, CreateView, DetailView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from blog.models import Post

import json
import random

from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.conf import settings


class PostList(ListView):
    model = Post
    template_name = 'index-new.html'

    def get_queryset(self):
        qs = super(PostList, self).get_queryset()
        return qs.order_by('-id')[:10]


def load_posts(request):

    post_list = Post.objects.all().order_by('-id')
    paginator = Paginator(post_list, 5)

    if request.method == 'GET':
        if request.is_ajax():

            page = request.GET.get('page')

            try:
                posts_paginator = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                # posts_paginator = paginator.page(2)
                return HttpResponseBadRequest()
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                # posts_paginator = paginator.page(paginator.num_pages)
                return HttpResponseBadRequest()


            posts_values = posts_paginator.object_list.values('slug', 'category', 'title', 'text_entry', 'image')

            for value in posts_values:
                value['image'] = settings.MEDIA_URL + value['image']

            posts_json = json.dumps(list(posts_values))

            return HttpResponse(posts_json)

        else:

            return render_to_response('index-new.html', {"object_list": paginator.page(1).object_list})



def recommendedPosts():
    posts = Post.objects.all().order_by('-views_count')[:100]

    last = Post.objects.count() - 1

    def generate():
        index1 = random.randint(0, last)
        index2 = random.randint(0, last)
        index3 = random.randint(0, last)
        index4 = random.randint(0, last)


    # if index2 == index1: index2 = last

    MyObj1 = Post.objects.all()[index1]
    MyObj2 = Post.objects.all()[index2]



class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'

    def get_object(self):

        object = super(PostDetail, self).get_object()
        object.views_count += 1
        object.save()

        return object

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)

        # posts = Post.objects.all().order_by('-id')[:4]

        posts = Post.objects.all().order_by('-views_count').exclude(id=self.get_object().id)[:100]

        context["recommended_posts"] = random.sample(list(posts), 4)
        return context


"""
        arguments_for_1 = Thread.objects.filter(holywar = holywar_data, argument_for = 1)
        arguments_for_1 = arguments_for_1.all().order_by('-thread_likes')[:5]


        page = self.request.GET.get('page')


        context["holywar"] = holywar_data

        context["arguments_for_1"] = arguments_for_1

        # context["comments_list"] = self.model.objects.filter(thread = holywar_data)
        # context["thread"] = get_object_or_404(Thread, pk=pk)

        return context
"""

"""
    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context["arguments_for_2"] = arguments_for_2

        context["comments_list"] = self.model.objects.filter(thread = holywar_data)
        context["thread"] = get_object_or_404(Thread, pk=pk)

        return context
"""
