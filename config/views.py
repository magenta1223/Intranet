from django.shortcuts import render, get_object_or_404, redirect
from bulletinboard.models import Category
from event.models import *
from event.utils import *
from django.db.models import Q


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


    context = {'categories' : categories, 'categories' : categories, 'vacations' : vacations_reforatted, 'tasks': tasks_reforatted}


    return render(request, 'landing.html', context)

