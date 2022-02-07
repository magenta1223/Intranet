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
from common.utils import is_authenticated
from config.settings import BASE_DIR


@login_required(login_url='common:login')
def index(request):
    """
    estimator list
    """
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')
    categories = Category.objects.all()

    estimator_list = Estimator.objects.order_by('-id')

    if kw:
        estimator_list = estimator_list.filter(
            Q(name__icontains=kw) |  # 제목검색
            Q(author__name__icontains=kw) #|  # 질문 글쓴이검색
        ).distinct()

    # paging 10 posts per page
    paginator = Paginator(estimator_list, 10)
    page_obj = paginator.get_page(page)

    context = {'estimator_list': page_obj, 'page': page, 'kw': kw, 'categories' : categories}

    return render(request, 'task/estimator_list.html', context)



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