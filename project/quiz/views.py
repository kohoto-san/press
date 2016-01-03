from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse

from quiz.models import Fact, Answer

import random
import json


def home(request):

    if request.method == 'GET':
        if request.is_ajax():

            #question = get_object_or_404(Question, id_question=id_question)
            #answers = Answer.objects.filter(question_id=question.id)

            # posts_values = posts_paginator.object_list.values('slug', 'category', 'title', 'text_entry', 'image')
            # for value in posts_values:
            #   value['image'] = settings.MEDIA_URL + value['image']
            # posts_json = json.dumps(list(posts_values))

            result = load_fact(request)
            # result.update([{'correct': 0}])

            result_json = json.dumps(list([result]))
            return HttpResponse(result_json)

            # context = {'question': question, 'answers': answers}
            # html = render_to_string('spectest/question.html', context)
            # return HttpResponse(html)

            # return HttpResponse(posts_json)

        else:
            # count_questions = Question.objects.all().count()
            # return render_to_response('spectest/index.html', {'count_questions': count_questions})
            return render_to_response('quiz/index.html')


def load_fact(request):

    all_facts = Fact.objects.all()
    count_facts = len(all_facts)

    fact = random.sample(list(all_facts), 1)[0]
    answer = fact.answer

    answers_another_list = Answer.objects.exclude(id=answer.id)
    answer_another = random.sample(list(answers_another_list), 1)[0]

    if random.randint(0, 1) == 0:
        answer, answer_another = answer, answer_another
    else:
        answer, answer_another = answer_another, answer

    result = {'fact': fact.text, 'answer': answer.name, 'answer_another': answer_another.name, 'factID': fact.id}

    return result


def save_answer(request):
    answer_str = request.GET.get('answer')
    fact_id = request.GET.get('factID')

    fact = get_object_or_404(Fact, pk=fact_id)

    result = load_fact(request)

    if fact.answer.name == answer_str:
        result.update({'correct': 1})
    else:
        result.update({'correct': 0})

    result_json = json.dumps(list([result]))
    return HttpResponse(result_json)
