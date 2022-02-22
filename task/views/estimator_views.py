# models
from bulletinboard.models import Category
from ..models import *
from common.models import Wrapper

# forms
from ..forms import EstimatorForm, ContainerForm

# utils
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from common.utils import to_json

# estimator func
from ..utils import *
import json
# donwload
from common.utils import *
from config.settings import BASE_DIR



@login_required(login_url='common:login')
def estimator_create(request):
    if request.method == 'POST':
        form = EstimatorForm(request.POST)
        if form.is_valid():
            # form.cleaned_data['subject']

            estimator = form.save(commit=False)
            estimator.author = request.user
            estimator.create_date = timezone.now()
            estimator.type = form.cleaned_data['type']
            estimator.name = f"{request.POST['customer']}-{request.POST['type']}-{timezone.now().strftime('%Y-%m-%d %H')}"
            # subclass도 가져오고, 해당 subclass의 field를 가져와서
            estimator.kwargs = { k : v for k, v in request.POST.items() if k != 'csrfmiddlewaretoken' and 'additional' not in k}
            additional_kwargs = { k : v for k, v in request.POST.items() if 'additional' in k }
            estimator.additional_kwargs = { additional_kwargs[f'additional_key{i}'] : additional_kwargs[f'additional_val{i}'] for i in range(1, (len(additional_kwargs) // 2) + 1)}

            prices = calc_closet(estimator.kwargs)
            estimator.prices = prices
            estimator.save()

            wrapper = Wrapper(estimator = estimator, create_date = estimator.create_date, author = estimator.author, app_name = 'task', content_name = 'estimator')
            wrapper.save()
            #render_esitmator(estimator)

            return redirect('task:index')
    else:
        # 처음 접근 시, GET을 사용 (링크를 통한 페이지 요청의 경우 GET을 사용한다)
        form = EstimatorForm()

    categories = Category.objects.all()
    types = EstimatorType.objects.all()
    context = {'form': form, 'categories' : categories, 'types' : types}
    return render(request, 'task/estimator_form.html', context)


@login_required(login_url='common:login')
def estimator_modify(request, estimator_id):
    estimator = get_object_or_404(Estimator, pk = estimator_id)
    # user verification
    if request.user != estimator.author:
        messages.error(request, '수정권한이 없습니다.')
        return redirect('task:detail', post_id=estimator.id)

    # submit modified
    if request.method == "POST":
        form = EstimatorForm(request.POST, instance=estimator)
        if form.is_valid():
            estimator = form.save(commit=False)
            estimator.modify_date = timezone.now()  # 수정일시 저장

            estimator.types = form.cleaned_data['type']
            estimator.kwargs = { k : v for k, v in request.POST.items() if k != 'csrfmiddlewaretoken' and 'additional' not in k}
            additional_kwargs = { k : v for k, v in request.POST.items() if 'additional' in k }
            estimator.additional_kwargs = { additional_kwargs[f'additional_key{i}'] : additional_kwargs[f'additional_val{i}'] for i in range(1, (len(additional_kwargs) // 2) + 1)}

            prices = calc_closet(estimator.kwargs)
            estimator.prices = prices
            estimator.save()

            return redirect('task:detail', wrapper_id=estimator.wrapper.id)
    else:
        form = EstimatorForm(instance=estimator)

        categories = Category.objects.all()
        types = EstimatorType.objects.all()
        context = {'form': form, 'categories' : categories, 'types' : types}
        return render(request, 'task/estimator_form.html', context)


@login_required(login_url='common:login')
def estimator_delete(request, estimator_id):
    estimator = get_object_or_404(Estimator, pk=estimator_id)
    # user verification
    if request.user != estimator.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('task:detail', estimator_id=estimator.id)
    estimator.delete()
    return redirect('task:index')


@login_required(login_url='common:login')
def estimator_download(request, estimator_id):

    # 처음 접근 시, GET을 사용 (링크를 통한 페이지 요청의 경우 GET을 사용한다)
    estimator = get_object_or_404(Estimator, pk = estimator_id)

    render_esitmator(estimator)

    file_path = os.path.join(BASE_DIR, f'data/{estimator.name}.xlsx')

    return download(request, file_path, f'{estimator.name}.xlsx')


@login_required(login_url='common:login')
def multi_estimator_create(request):
    if request.method == 'POST':
        form = EstimatorForm(request.POST)
        if form.is_valid():
            # form.cleaned_data['subject']

            estimator = form.save(commit=False)
            estimator.author = request.user
            estimator.create_date = timezone.now()
            estimator.type = form.cleaned_data['type']
            estimator.name = f"{request.POST['customer']}-{request.POST['type']}-{timezone.now().strftime('%Y-%m-%d %H')}"
            # subclass도 가져오고, 해당 subclass의 field를 가져와서
            estimator.kwargs = { k : v for k, v in request.POST.items() if k != 'csrfmiddlewaretoken' and 'additional' not in k}
            additional_kwargs = { k : v for k, v in request.POST.items() if 'additional' in k }
            estimator.additional_kwargs = { additional_kwargs[f'additional_key{i}'] : additional_kwargs[f'additional_val{i}'] for i in range(1, (len(additional_kwargs) // 2) + 1)}

            prices = calc_closet(estimator.kwargs)
            estimator.prices = prices
            estimator.save()

            wrapper = Wrapper(estimator = estimator, create_date = estimator.create_date, author = estimator.author, app_name = 'task', content_name = 'estimator')
            wrapper.save()
            #render_esitmator(estimator)

            return redirect('task:index')
    else:
        # 처음 접근 시, GET을 사용 (링크를 통한 페이지 요청의 경우 GET을 사용한다)
        pass

    categories = Category.objects.all()
    types = EstimatorType.objects.all()

    print(types[0].kwargs)

    context = { 'categories' : categories, 'types' : types}
    return render(request, 'task/multi_estimator.html', context)


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
def estimator_create2(request):

    #print(json.loads(request.POST['json']))


    estimator_kwargs= request.POST.dict()#json.loads(request.POST)

    type = estimator_kwargs['type']   
    del  estimator_kwargs['type'],estimator_kwargs['csrfmiddlewaretoken']
    

    estimator = Estimator(kwargs= estimator_kwargs)

    estimator.author = request.user
    estimator.create_date = timezone.now()
    estimator.type = type
    estimator.name = 'test' #f"{request.POST['customer']}-{request.POST['type']}-{timezone.now().strftime('%Y-%m-%d %H')}"
    # subclass도 가져오고, 해당 subclass의 field를 가져와서
    #additional_kwargs = { k : v for k, v in request.POST.items() if 'additional' in k }
    #estimator.additional_kwargs = { additional_kwargs[f'additional_key{i}'] : additional_kwargs[f'additional_val{i}'] for i in range(1, (len(additional_kwargs) // 2) + 1)}

    prices = calc_closet(estimator.kwargs)
    estimator.prices = prices    
    estimator.save()

    wrapper = Wrapper(estimator = estimator, create_date = estimator.create_date, author = estimator.author, app_name = 'task', content_name = 'estimator')
    wrapper.save()

    


    #estimator_kwargs = json.loads(request.POST['json'])
    

    context = {'id' : wrapper.id}

    return JsonResponse(  context  )




    #return redirect('task:index')
