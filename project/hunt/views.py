from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string

from hunt.models import Post, Comment, Profile, Invite
from hunt.forms import CommentForm

from collections import OrderedDict
from collections import defaultdict
from itertools import groupby
from unidecode import unidecode
import json

from django.core.serializers.json import DjangoJSONEncoder
from django.utils.text import slugify
# from django.template.defaultfilters import slugify

# class PostList(ListView):
    # model = Post
    # template_name = 'hunt/hunt.html'


def post_list(request):
    return render(request, 'hunt/hunt.html')


def load_posts(request):

    if request.method == 'GET':
        if request.is_ajax():

            # test_post_list = Post.objects.values('date_create', 'pk', 'title', 'description').order_by('-time_create')
            # test_list = groupby(test_post_list, lambda obj: obj.time_create)

            profile_id = request.GET.get('profile')

            if profile_id:
                post_objects = Post.objects.filter(upvotes=profile_id).order_by('-time_create')
            else:
                post_objects = Post.objects.order_by('-time_create')

            if not post_objects:
                return HttpResponse('empty')

            post_list = groupby(post_objects, lambda x: x.date_create)

            res = []
            for date, posts in post_list:
                date_post_list = list(posts)

                date_post_list.sort(key=lambda item: item.upvotes_count, reverse=True)

                # print( sorted(date_post_list, key=lambda item: item.upvotes.count(), reverse=True) )

                # newlist = sorted(date_post_list, key=lambda x: x.upvotes.count, reverse=True)
                date_post_list.insert(0, date)
                res.append(date_post_list)

                """
                date_post_list = []
                date_post_list.append(date)
                for post in posts:
                    date_post_list.append(post)
                res.append(date_post_list)
                """
            # posts_json = json.dumps(res, cls=DjangoJSONEncoder)
            paginator = Paginator(res, 15)

            page = request.GET.get('page')

            try:
                posts_paginator = paginator.page(page)
            except PageNotAnInteger:
                return HttpResponseBadRequest()
            except EmptyPage:
                return HttpResponseBadRequest()

            context = {'object_list': posts_paginator.object_list, 'user': request.user}

            html = render_to_string('hunt/post-list.html', context)
            return HttpResponse(html)


    # dates = model.objects.filter(**params).only(*only).order_by('event_date')
    # dates = groupby(dates, lambda obj: obj.event_date)


class PostCreate(CreateView):
    model = Post
    template_name = 'hunt/create_post.html'

    fields = ['title', 'description', 'link']

    def form_valid(self, form):
        if self.request.user.is_authenticated():

            title = unidecode(form.instance.title)
            slug = slugify(title, allow_unicode=True)
            num_iteration = 2
            slug_exist = False

            while(Post.objects.filter(slug=slug)):
                if slug_exist:
                    slug = slug[:slug.rfind('-')]
                else:
                    slug_exist = True

                slug += '-%d' % num_iteration
                num_iteration += 1

            profile = self.request.user.profile

            form.instance.author = profile
            form.instance.slug = slug

            post = form.save()

            post.upvotes.add(profile)
            post.save()

            return super(PostCreate, self).form_valid(form)

        else:
            return HttpResponseRedirect('/startups')

    def get_success_url(self):
        return reverse('hunt:post_detail', args=(self.object.slug,))

    def dispatch(self, request, *args, **kwargs):

        if not self.request.user.is_authenticated():
            return HttpResponseRedirect('/startups')
        else:
            return super(PostCreate, self).dispatch(request, *args, **kwargs)


class PostDetail(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'hunt/post.html'

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)

        post = get_object_or_404(Post, slug=self.kwargs['slug'])
        comments = Comment.objects.filter(post=post)

        context['object'] = post
        context['comments'] = comments

        return context

    def form_valid(self, form):
        if self.request.user.is_authenticated():

            post = get_object_or_404(Post, slug=self.kwargs['slug'])
            profile = self.request.user.profile

            form.instance.profile = profile
            form.instance.post = post

            post = form.save()

            return super(PostDetail, self).form_valid(form)

    def get_success_url(self):
        return reverse('hunt:post_detail', args=(self.object.post.slug,))


def vote(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user.is_authenticated() and request.method == 'POST':
        user = request.user.profile
        method = request.POST.get('method')
        if method == 'CREATE':
            post.upvotes.add(user)
            # post.upvotes_count += 1
            post.save()
            return HttpResponse('OK')
        if method == 'DELETE':
            post.upvotes.remove(user)
            # post.upvotes_count -= 1
            post.save()
            return HttpResponse('OK')
    else:
        raise Http404

"""
class ProfileDetails(DetailView):
    model = Profile
    template_name = 'hunt/profile.html'
"""


def profile_details(request, id_profile):
    profile = get_object_or_404(Profile, id_profile=id_profile)
    return render(request, 'hunt/profile.html', {'profile': profile})

"""
class ProfileDetail(UpdateView):
    model = Invite
    template_name = 'hunt/profile.html'
    fields = ['text']

    def get_context_data(self, **kwargs):
        context = super(ProfileDetail, self).get_context_data(**kwargs)

        profile = get_object_or_404(Profile, id_profile=self.kwargs['id_profile'])
        context['profile'] = profile
        return context

    def get_success_url(self):
        print(self.object.user.pk)
        return reverse('hunt:profile_details', args=(self.object.user.pk,))
"""


def invite(request):
    if request.user.is_authenticated() and request.method == 'POST':
        invite_text = request.POST.get('invite_text')
        invite = Invite.objects.filter(text=invite_text).first()
        if invite and not invite.profile:
            user = request.user.profile
            user.type_profile = user.ACTIVE
            user.save()

            invite.profile = user
            invite.save()
            return HttpResponse('OK')

        else:
            return HttpResponse('incorrect')


def redirect(request):
    if request.method == 'GET':
        url = request.GET.get('url')
        return HttpResponseRedirect(url)
