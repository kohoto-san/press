from django.contrib import admin
from django import forms
from django.forms.formsets import formset_factory

from blog.models import Post, Author, Category, Image


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

    def save_model(self, request, obj, form, change):
        if form.is_valid():
            if not obj.id_post:
                count = Post.objects.count() - 1
                post = Post.objects.all().order_by('-id_post').first()

                obj.id_post = post.id_post + 1

                obj.save()
            else:
                obj.save()


admin.site.register(Post, PostAdmin)


admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Image)


""""
class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']


class PersonAdmin(admin.ModelAdmin):
    exclude = ['age']
    form = PersonForm

class ImageInline(admin.StackedInline):
    model = Image
    # extra = 3
    ImageFormSet = formset_factory(ImageForm)
"""
