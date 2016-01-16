from django.shortcuts import render, render_to_response, get_object_or_404

from django.views.generic import ListView, CreateView, DetailView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from blog.models import Post, Typo, SubscribeEmail, NewContact, Headline, ExternalLink

import json
import random

from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.conf import settings

from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse

from django.utils.feedgenerator import Rss201rev2Feed
from django.template.loader import render_to_string

from django.http import Http404

from blog.forms import SubscribeEmailForm


class NewContactCreate(CreateView):
    model = NewContact
    template_name = 'contacts.html'

    fields = ['name', 'email', 'text']

    def form_valid(self, form):
        # form.save()
        # return super(ContactCreate, self).form_valid(form)

        return HttpResponseRedirect('?success')
        # return render_to_response('contacts.html', {'form' 'fuck': 'fuck'})

    """
    def get_success_url(self):
        return HttpResponse('oh shit')
        # return reverse('holywar_detail', args=(self.object.id,))
    """


class CorrectMimeTypeFeed(Rss201rev2Feed):
    mime_type = 'application/xml'


class LatestEntriesFeed(Feed):
    # feed_type = CorrectMimeTypeFeed
    title = "StartupDen.ru"
    link = "/"
    # description = "Updates on changes and additions to police beat central."

    def items(self):
        return Post.objects.all().order_by('-id_post')[:20]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.text_entry

    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, item):
        return reverse('post_detail', args=[item.slug])

    item_enclosure_mime_type = "image/jpeg"

    def item_enclosure_url(self, item):
        return 'http://startupden.ru' + item.image.url

    def item_pubdate(self, item):
        return item.date


# published_feeds = {'mlist': LatestEntriesFeed}


class HeadlineList(ListView):
    model = Headline
    template_name = 'headline.html'

    def get_queryset(self):
        qs = super(HeadlineList, self).get_queryset()
        return qs.order_by('-date')


def link(request, slug):

    try:
        link = ExternalLink.objects.get(internal=slug)
        return HttpResponseRedirect(link.external)
    except ExternalLink.DoesNotExist:
        raise Http404()


class PostList(ListView):
    model = Post
    template_name = 'index-new.html'

    def get_queryset(self):
        qs = super(PostList, self).get_queryset()
        return qs.order_by('-id')[:10]


def load_home(request):
    post_list_home = Post.objects.all().order_by('-id_post')
    # print('load_home')
    return load_posts(request, post_list_home, 'home')


def load_news(request):
    post_list_news = Post.objects.filter(category__text="News").order_by('-id_post')
    # print('load_news')
    return load_posts(request, post_list_news, 'news')


def load_articles(request):
    post_list_art = Post.objects.exclude(category__text="News").order_by('-id_post')
    # print('load_articles')
    return load_posts(request, post_list_art, 'articles')


def load_posts(request, post_list, type_page):

    feat_posts_count = Post.objects.exclude(category__text="News").values_list('pk', flat=True)
    feat_posts_id = random.sample(list(feat_posts_count), 4)

    feat_posts = Post.objects.filter(pk__in=[pk_post for pk_post in feat_posts_id])

    paginator = Paginator(post_list, 10)

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

            # posts_values = posts_paginator.object_list.values('slug', 'category', 'title', 'text_entry', 'image')

            # for value in posts_values:
            #   value['image'] = settings.MEDIA_URL + value['image']

            # posts_json = json.dumps(list(posts_values))

            context = {'object_list': posts_paginator.object_list}
            html = render_to_string('card-posts-ajax.html', context)
            return HttpResponse(html)

            # return HttpResponse(posts_json)

        else:
            form = SubscribeEmailForm(label_suffix='')
            news = Headline.objects.all().order_by('-date')[:10]
            if type_page != "articles":
                return render_to_response('index-new.html', {'feat_posts': feat_posts, 'form': form, 'news_list': news})
            else:
                return render_to_response('index-posts.html', {'feat_posts': feat_posts, 'form': form, 'news_list': news})

            # return render_to_response('index-new.html', {"object_list": paginator.page(1).object_list})

    post_list = None


def email_create(request):

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SubscribeEmailForm(request.POST)

        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            p = SubscribeEmail.objects.create(email=form.cleaned_data['email'])
            p.save()
            return HttpResponse('valid')
        else:
            if request.is_ajax():
                # Prepare JSON for parsing
                errors_dict = {}
                if form.errors:
                    for error in form.errors:
                        e = form.errors[error]
                        errors_dict[error] = e
                        # errors_dict[error] = unicode(e)

                print(form.errors)
                return HttpResponseBadRequest(json.dumps(errors_dict))

            # return HttpResponse('NO valid')

    # if a GET (or any other method) we'll create a blank form
    else:
        return HttpResponseRedirect('/')
        # form = PersonForm()


def typo_send(request):

    if request.method == 'POST' and request.is_ajax():
        id_post = request.POST['pk']
        text = request.POST['text']

        try:
            post = Post.objects.filter(id=id_post)[0]
            Typo.objects.create(post=post, text=text)
            return HttpResponse('sent')
        except IndexError:
            return HttpResponse('no_sent')

    else:
        return HttpResponseRedirect('/')


"""
        obj, created = ThreadCommentsLike.objects.get_or_create(comment = comment, user = request.user)

        if created == True:
            comment.comment_likes += 1
            comment.save()
            return HttpResponse('liked')
        else:
            return HttpResponse('no_liked')
"""


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

        posts = Post.objects.all().order_by('-views_count').exclude(id=self.object.id)[:100]

        current_post_id = self.object.id_post

        next_post = Post.objects.filter(id_post=current_post_id + 1).first()
        prev_post = Post.objects.filter(id_post=current_post_id - 1).first()

        context["recommended_posts"] = random.sample(list(posts), 8)

        if next_post:
            context["next_post"] = next_post

        if prev_post:
            context["prev_post"] = prev_post

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
