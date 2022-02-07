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

@login_required(login_url='common:login')
def profile(request):
    """
    계정생성
    """

    user = request.user
    categories = Category.objects.all()  # 전체 카테고리



    # 휴가는 작성자가 본인임
    vacations = Vacation.objects.filter(
        Q(author__id__iexact=user.id)
    )

    tasks = Task.objects.filter(
        Q(user__id__iexact=user.id)
    )


    vacations_reforatted = reformat(vacations, vacation = True)
    tasks_reforatted = reformat(tasks)


    context = {'user' : user , 'categories' : categories, 'categories' : categories, 'vacations' : vacations_reforatted, 'tasks': tasks_reforatted}


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