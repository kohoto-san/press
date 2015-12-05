from django.shortcuts import render

from django.views.generic import ListView, CreateView, DetailView

from blog.models import Post


class PostList(ListView):
    model = Post
    template_name = 'index.html'

    def get_queryset(self):
        qs = super(PostList, self).get_queryset()
        return qs.order_by('-id')[:10]


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'

"""
    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context["arguments_for_2"] = arguments_for_2

        context["comments_list"] = self.model.objects.filter(thread = holywar_data)
        context["thread"] = get_object_or_404(Thread, pk=pk)

        return context
"""