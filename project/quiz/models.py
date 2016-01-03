from django.db import models


# Company / Startuper
class Answer(models.Model):

    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Answer"
        verbose_name_plural = "Answers"

    def __str__(self):
        return self.name


class Fact(models.Model):

    text = models.TextField()
    answer = models.ForeignKey(Answer)

    class Meta:
        verbose_name = "Fact"
        verbose_name_plural = "Facts"

    def __str__(self):
        return self.text
