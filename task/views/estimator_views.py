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

        estimator.kwargs = v
        #estimator.name = f"{request.POST['customer']}-{request.POST['type']}-{timezone.now().strftime('%Y-%m-%d %H')}"
        # subclass도 가져오고, 해당 subclass의 field를 가져와서
        #estimator.kwargs = { k : v for k, v in request.POST.items() if k != 'csrfmiddlewaretoken' and 'additional' not in k}
        #additional_kwargs = { k : v for k, v in request.POST.items() if 'additional' in k }
        #estimator.additional_kwargs = { additional_kwargs[f'additional_key{i}'] : additional_kwargs[f'additional_val{i}'] for i in range(1, (len(additional_kwargs) // 2) + 1)}
        
        # func_dict에서 가져와서 쓰도록
        prices = FUNC_DICT[estimator.type](estimator.kwargs)
        estimator.prices = prices
        estimator.save()


        container.estimator_set.add(estimator)

    container.save()    
    wrapper = Wrapper(container = container, create_date = timezone.now(), author = request.user, app_name = 'task', content_name = 'container')
    wrapper.save()

    return JsonResponse(  {}  )




