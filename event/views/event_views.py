from django.shortcuts import render

# Create your views here.

# models
from bulletinboard.models import Category
from ..models import *
from ..forms import VacationForm
from common.models import Wrapper, User

# utils
from django.shortcuts import render, get_object_or_404, resolve_url, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone

# donwload
from common.utils import is_authenticated
from config.settings import BASE_DIR


@login_required(login_url='common:login')
def calendar_view(request):
    """
    """

    categories = Category.objects.all()  # 전체 카테고리

    # 휴가는 작성자가 본인임
    vacations = Vacation.objects.all()

    tasks = Task.objects.all()

    vacations_reforatted = reformat(vacations, vacation = True)
    tasks_reforatted = reformat(tasks)


    context = {'categories' : categories, 'categories' : categories, 'vacations' : vacations_reforatted, 'tasks': tasks_reforatted}


    return render(request, 'common/profile.html', context)

@login_required(login_url='common:login')
def vacation_request(request):
    """
    request vacation of user
    Todo:

    """
    if request.method == 'POST':
        form = VacationForm(request.POST)
        if form.is_valid():
            vacation = form.save(commit=False)

            print(vacation.description)
            vacation.author = request.user
            user = User.objects.get(id = request.user.id)
            vacation.status = '1' # for requested
            vacation.name = f'{request.user.name} 휴가'
            vacation.create_date = timezone.now()

            print(vacation.start, vacation.end)

            vacation.save()

            # manytomany에 저장하려면 두 객체가 모두 저장되어 있어야 한다.
            vacation.user.add(request.user)
            vacation.save()

            return redirect('common:profile')

    else:
        categories = Category.objects.all()

        form = VacationForm()
        context = {'form': form, 'categories' : categories}
        return render(request, 'event/vacation_form.html', context)



