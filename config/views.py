from django.shortcuts import render, get_object_or_404, redirect
from bulletinboard.models import Category
from event.models import *
from event.utils import *
from django.db.models import Q
from event.models import *
import json


def landing(request):
    categories = Category.objects.all()
    context = {'categories' : categories}

    categories = Category.objects.all()  # 전체 카테고리

    vacations = Vacation.objects.filter(
        Q(status__iexact = '2')
    )


    tasks = Task.objects.all()

    vacations_reforatted = reformat(vacations, vacation = True)
    tasks_reforatted = reformat(tasks)

    color_dict = { config.name : config.color for i, config in enumerate(TaskConfig.objects.all())}

    color_dict['지나간 휴가'] = '#DCDCDC'  # 회색. 지나감
    #color_dict['승인 대기중인 휴가'] = '#BDE3DD'  # 연한 초록색. 승인 대기중
    color_dict['예정된 휴가'] = '#03BD9E'  # 승인
    #color_dict['반려된 휴가'] = '#FF4040'  # 반려

    color_dict_json = json.dumps(color_dict)



    context = {'categories' : categories, 'categories' : categories, 'vacations' : vacations_reforatted, 'tasks': tasks_reforatted,  'color_dict':color_dict, 'color_dict_json' : color_dict_json}


    return render(request, 'landing.html', context)

