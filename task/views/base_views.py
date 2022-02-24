# models
from bulletinboard.models import Category
from ..models import Estimator
from common.models import Wrapper

# utils
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# donwload
from config.settings import BASE_DIR
from utils import *


@login_required(login_url='common:login')
def detail(request, wrapper_id):
    """
    estimator detail
    """
    wrapper = get_object_or_404(Wrapper, pk=wrapper_id)
    estimator = wrapper.estimator
    categories = Category.objects.all()
    context = {'categories': categories, 'estimator' : estimator}

    return render(request, 'task/estimator_detail.html', context)


@login_required(login_url='common:login')
def multi_index(request):
    """
    estimator list
    """
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')
    categories = Category.objects.all()

    #estimator_list = Estimator.objects.order_by('-id')

    # 어차피 이건.. 쓰지도 않을건데 
    wrappers = Wrapper.objects.all().filter(
        Q(content_name__iexact = 'container')
        ).order_by('-id')

    container_list = [ wrapper.container for wrapper in wrappers]

    if kw:
        container_list = container_list.filter(
            Q(name__icontains=kw) |  # 제목검색
            Q(author__name__icontains=kw) #|  # 질문 글쓴이검색
        ).distinct()

    # paging 10 posts per page
    paginator = Paginator(container_list, 10)
    page_obj = paginator.get_page(page)

    context = {'container_list': page_obj, 'page': page, 'kw': kw, 'categories' : categories}

    return render(request, 'task/container_list.html', context)


@login_required(login_url='common:login')
def multi_detail(request, wrapper_id):
    """
    estimator detail
    """
    wrapper = get_object_or_404(Wrapper, pk=wrapper_id)
    container = wrapper.container
    categories = Category.objects.all()
    context = {'categories': categories, 'container' : container}

    return render(request, 'task/container_detail.html', context)