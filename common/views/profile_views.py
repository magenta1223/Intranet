# models
from ..models import User
from bulletinboard.models import Category
from event.models import *
# forms
from ..forms import UserChangeForm

# utils
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone
from utils import *
from django.http import JsonResponse, HttpResponse

import json


@login_required(login_url='common:login')
def profile(request):
    """
    계정생성
    """
    user = request.user
    categories = Category.objects.all()  # 전체 카테고리


    # --------------------------------- #
    task_colors = { config.name : config.color for i, config in enumerate(TaskConfig.objects.all())}
    vac_colors = {}
    vac_colors['지나감'] = '#DCDCDC'  # 회색. 지나감
    vac_colors['승인 대기'] = '#BDE3DD'  # 연한 초록색. 승인 대기중
    vac_colors['예정'] = '#03BD9E'  # 승인
    vac_colors['반려'] = '#FF4040'  # 반려

    vac_colors_json = json.dumps(vac_colors)
    task_colors_json = json.dumps(task_colors)

    # --------------------------------- #

    # 휴가는 작성자가 본인임
    vacations = Vacation.objects.filter(
        Q(author__id__iexact=user.id)

    )

    tasks = Task.objects.filter(
        Q(user__id__iexact=user.id)
    )


    # reformat
    vacations = json.dumps(reformat(vacations, vacation = True))
    tasks = json.dumps(reformat(tasks, vacation = False))



    context = {'user' : user ,
               'categories' : categories,
               'vacations' : vacations,
               'tasks': tasks,
               'vac_colors' : vac_colors,
               'vac_colors_json' : vac_colors_json,
               'task_colors': task_colors,
               'task_colors_json' : task_colors_json

               }


    return render(request, 'common/profile.html', context)


@login_required(login_url='common:login')
def profile_modify(request):
    """
    계정생성
    """

    req_user = request.user
    categories = Category.objects.all()  # 전체 카테고리
    req_user = get_object_or_404(User, pk = req_user.id)

    if request.method == "POST":

        form = UserChangeForm(request.POST, instance = req_user)

        if form.is_valid():
            user = form.save(commit=False)
            user.modify_date = timezone.now()  # 수정일시 저장
            user.save()
            return redirect('common:profile')
        else:
            print(form.errors)

    else:
        form = UserChangeForm()
        context = { 'user' : req_user , 'categories' : categories, 'form' : form}

        return render(request, 'common/profile_modify.html', context)