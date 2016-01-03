from django.contrib import admin
from spectest.models import Question, Answer, Result, Point


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]


class PointInline(admin.TabularInline):
    model = Point
    extra = 3


class AnswerAdmin(admin.ModelAdmin):
    inlines = [PointInline]


admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)

admin.site.register(Result)
admin.site.register(Point)
