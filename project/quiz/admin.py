from django.contrib import admin
from quiz.models import Fact, Answer


class FactInline(admin.TabularInline):
    model = Fact
    extra = 3


class AnswerAdmin(admin.ModelAdmin):
    inlines = [FactInline]


admin.site.register(Answer, AnswerAdmin)
admin.site.register(Fact)
