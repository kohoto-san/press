from django.shortcuts import render, render_to_response, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse

from django.views.generic import DetailView


from spectest.models import Question, Answer, Result, Point


def home(request):

    if request.method == 'GET':
        if request.is_ajax():

            id_question = request.GET.get('q')

            question = get_object_or_404(Question, id_question=id_question)
            answers = Answer.objects.filter(question_id=question.id)

            # posts_values = posts_paginator.object_list.values('slug', 'category', 'title', 'text_entry', 'image')

            # for value in posts_values:
            #   value['image'] = settings.MEDIA_URL + value['image']

            # posts_json = json.dumps(list(posts_values))

            context = {'question': question, 'answers': answers}
            html = render_to_string('spectest/question.html', context)
            return HttpResponse(html)

            # return HttpResponse(posts_json)

        else:
            count_questions = Question.objects.all().count()
            return render_to_response('spectest/index.html', {'count_questions': count_questions})


def result_calc(request):
    if request.method == 'GET':
        if request.is_ajax():

            # Получаю list с IDшниками ответов
            id_answers = request.GET.get('answers').split(',')
            answers = Answer.objects.filter(pk__in=id_answers)

            results_values = Result.objects.all().values('name')
            results_list = []

            for result_value in results_values:
                results_list.append(result_value['name'])

            results = dict.fromkeys(results_list, 0)

            total_points = []

            for answer in answers:
                points = answer.point_set.all().values('result__name', 'points')
                for point in points:
                    total_points.append(point)

            for total_point in total_points:
                name_result = total_point['result__name']
                results[name_result] += total_point['points']

            result_name = max(results, key=(lambda k: results[k]))
            total_result = get_object_or_404(Result, name=result_name)

            return HttpResponse(total_result.slug)
