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

    # reformat
    vacations = json.dumps(reformat(vacations, vacation = True))
    tasks = json.dumps(reformat(tasks, vacation = False))



    task_colors = { config.name : config.color for i, config in enumerate(TaskConfig.objects.all())}
    vac_colors = {}
    vac_colors['지나감'] = '#DCDCDC'  # 회색. 지나감
    vac_colors['예정'] = '#03BD9E'  # 승인

    vac_colors_json = json.dumps(vac_colors)
    task_colors_json = json.dumps(task_colors)


    context = {'categories' : categories,
               'vacations' : vacations,
               'tasks': tasks,
               'vac_colors' : vac_colors,
               'vac_colors_json' : vac_colors_json,
               'task_colors': task_colors,
               'task_colors_json' : task_colors_json

               }



    return render(request, 'landing.html', context)

