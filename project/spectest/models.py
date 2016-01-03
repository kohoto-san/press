from django.db import models

# Create your models here.


class Question(models.Model):

    text = models.TextField()
    id_question = models.IntegerField()

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    def __str__(self):
        return self.text


class Answer(models.Model):

    question = models.ForeignKey(Question)
    text = models.TextField()

    class Meta:
        verbose_name = "Answer"
        verbose_name_plural = "Answers"

    def __str__(self):
        return self.text


class Result(models.Model):

    name = models.CharField(max_length=255)
    text = models.TextField()
    slug = models.SlugField()

    class Meta:
        verbose_name = "Result"
        verbose_name_plural = "Results"

    def __str__(self):
        return self.name


class Point(models.Model):

    answer = models.ForeignKey(Answer)
    result = models.ForeignKey(Result)
    points = models.IntegerField()

    class Meta:
        verbose_name = "Point"
        verbose_name_plural = "Points"

    def __str__(self):
        return "Ответив ——" + self.answer.text + "—— получишь " + str(self.points) + " для " + self.result.name
