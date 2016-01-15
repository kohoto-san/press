from django.db import models
import yaml


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

    def save(self, *args, **kwargs):
        if not self.id:
            stream = self.content.read()
            text_list = yaml.load(stream)

            for company in text_list:
                facts = text_list[company]
                answer = Answer.objects.create(name=company)
                for fact in facts:
                    Fact.objects.create(text=fact, answer=answer)

        return super(TextContent, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "TextContent"
        verbose_name_plural = "TextContents"

    def __str__(self):
        return self.content.url
