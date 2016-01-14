from django.db import models


# Company / Startuper
class Answer(models.Model):

    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Answer"
        verbose_name_plural = "Answers"

    def __str__(self):
        return self.name


# Question
class Fact(models.Model):

    text = models.TextField()
    answer = models.ForeignKey(Answer, related_name='fact')

    class Meta:
        verbose_name = "Fact"
        verbose_name_plural = "Facts"

    def __str__(self):
        return self.text


class TextContent(models.Model):

    content = models.FileField(upload_to='files', null=True)

    class Meta:
        verbose_name = "TextContent"
        verbose_name_plural = "TextContents"

    def __str__(self):
        return self.content
