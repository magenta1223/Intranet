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
from event.utils import *
from django.http import JsonResponse, HttpResponse

import json


@login_required(login_url='common:login')
def profile(request):
    """
    계정생성
    """
    user = request.user
    categories = Category.objects.all()  # 전체 카테고리

    vacations = []

    '#DCDCDC' # 회색. 지나감
    '#BDE3DD' # 연한 초록색. 승인 대기중
    '#03BD9E' # 승인
    '#FF4040' # 반려

    color_dict = { config.name : config.color for i, config in enumerate(TaskConfig.objects.all())}

    color_dict['지나간 휴가'] = '#DCDCDC'  # 회색. 지나감
    color_dict['승인 대기중인 휴가'] = '#BDE3DD'  # 연한 초록색. 승인 대기중
    color_dict['예정된 휴가'] = '#03BD9E'  # 승인
    color_dict['반려된 휴가'] = '#FF4040'  # 반려

    color_dict_json = json.dumps(color_dict)


    # 휴가는 작성자가 본인임
    vacations = Vacation.objects.filter(
        Q(author__id__iexact=user.id)

    )

    tasks = Task.objects.filter(
        Q(user__id__iexact=user.id)
    )


    vacations_reforatted = reformat(vacations, vacation = True)
    tasks_reforatted = reformat(tasks)


    context = {'user' : user , 'categories' : categories, 'vacations' : vacations_reforatted, 'tasks': tasks_reforatted, 'color_dict' : color_dict, 'color_dict_json' : color_dict_json}


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