# models
from bulletinboard.models import Category
from ..models import *
from common.models import Wrapper

# forms
from ..forms import ContainerForm

# utils
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from common.utils import to_json

# estimator func
import json
# donwload
from utils import *
from config.settings import BASE_DIR




@login_required(login_url='common:login')
def estimator_download(request, estimator_id):

    # 처음 접근 시, GET을 사용 (링크를 통한 페이지 요청의 경우 GET을 사용한다)
    estimator = get_object_or_404(Estimator, pk = estimator_id)

    render_esitmator(estimator)

    file_path = os.path.join(BASE_DIR, f'data/{estimator.name}.xlsx')

    return download(request, file_path, f'{estimator.name}.xlsx')

@login_required(login_url='common:login')
def container_download(request, container_id):

    container = get_object_or_404(EstimatorContainer, pk = container_id)

    render_container(container)

    file_path = os.path.join(BASE_DIR, f'data/{container.name}.xlsx')

    return download(request, file_path, f'{container.name}.xlsx')



@login_required(login_url='common:login')
def container_create(request):
    if request.method == 'POST':
        return redirect('task:container_index')
    else:
        # 처음 접근 시, GET을 사용 (링크를 통한 페이지 요청의 경우 GET을 사용한다)
        categories = Category.objects.all()
        types = EstimatorType.objects.all()

        context = { 'categories' : categories, 'types' : types}
        return render(request, 'task/multi_estimator.html', context)


@login_required(login_url='common:login')
def estimator_add(request):
    """
    Add new estimator in multi-estimator container
    """
    e_type = EstimatorType.objects.filter( type =  request.POST['type'])[0]

    kwargs = e_type.kwargs

    categories = to_json(Category.objects.all())
    types = to_json(EstimatorType.objects.all())
    context = {'categories' : categories, 'types' : types, 'kwargs' : kwargs}

    return JsonResponse(  context  )

@login_required(login_url='common:login')
def estimator_create(request):
    """
    Create estimators

    수량 추가
    견적서 보기 예쁘게 다듬고
    네이밍 룰하고

    알림 기능
    정도 .. ? 

    """

    data = json.loads(request.POST.dict()['data'])
    
    container = EstimatorContainer(
        author = request.user,
        create_date = timezone.now(),
        name = 'test'
    )
    
    container.save()
    

    for k, v in data.items():
        

        estimator = Estimator(
            type = v['type'],
        )

        del v['type']

        # key값을 유지해야함
        # 근데 보여줄 때는 name으로 보여줘야 한다
        
        kwargs = { _k : int(_v['value']) for _k, _v in v.items() if 'add' not in _k}
        estimator.kwargs = { _v['name'] : int(_v['value']) for _k, _v in v.items() if 'add' not in _k}
        estimator.additional_kwargs = {_v['name'] : int(_v['value']) for _k, _v in v.items() if 'add' in _k}

        # func_dict에서 가져와서 쓰도록
        prices = FUNC_DICT[estimator.type](kwargs)
        estimator.prices = prices
        estimator.save()


        container.estimator_set.add(estimator)


    container.save()    
    wrapper = Wrapper(container = container, create_date = timezone.now(), author = request.user, app_name = 'task', content_name = 'container')
    wrapper.save()

    return JsonResponse(  {}  )




