# models
from ..models import Level

# forms
from ..forms import UserCreateForm

# utils
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models import Q


def signup(request):
    """
    계정생성
    """
    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            date_of_birth = form.cleaned_data.get('date_of_birth')
            name = form.cleaned_data.get('name')
            create_date = timezone.now()

            levels = Level.objects.all()
            level = levels.filter(
                Q(level__icontains='Dummy')).distinct()[0]

            authenticate(username=email, password=raw_password, date_of_birth = date_of_birth, name = name, create_date = create_date)
            user.create_date = create_date
            user.level = level
            user.save()
            #login(request, user)
            #is_active = False 상태에서 login을 강제로 시킬 수가 없어서 에러가 발생..
            return redirect('index')
    else:
        form = UserCreateForm()
    return render(request, 'common/signup.html', {'form': form})