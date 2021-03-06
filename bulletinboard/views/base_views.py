from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from ..models import Post, Category
from common.models import Wrapper

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from utils import *



@login_required(login_url='common:login')
def index(request):
    """
    bulletinboard 목록 출력
    Done:
    1) Category를 render에 넘겨서 그에 맞는 상단 바 생성
    2) Category별로 post_list를 생성
    3) landing page
        1) landing page를 만들고
        2) category별 게시판 링크를 nav에 걸고
        3) 그러면 category id를 얻을 수 있겠죠?

    """
    # 입력 파라미터
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    categories = Category.objects.all()  # 전체 카테고리

    # 글 목록조회
    post_list = Post.objects.order_by('-create_date')

    if kw:
        post_list = post_list.filter(
            Q(title__icontains=kw) |  # 제목검색
            Q(content__icontains=kw) |  # 내용검색
            Q(author__name__icontains=kw) |  # 질문 글쓴이검색
            Q(reply__author__name__icontains=kw)  # 답변 글쓴이검색
        ).distinct()

    # 페이징처리
    paginator = Paginator(post_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'post_list': page_obj, 'page': page, 'kw': kw, 'categories' : categories}

    return render(request, 'bulletinboard/post_list.html', context)

@login_required(login_url='common:login')
def detail(request, wrapper_id):
    """
    view detailed contents of the post from pybo.detail

    Todo:

    Done:
    1) category에 따라서 상단바 생성할 수 있도록 category를 context에 넘겨주기 -> Done!

    """

    wrapper = get_object_or_404(Wrapper, pk=wrapper_id)
    post = wrapper.post

    cat_name = str(post.category)
    view_name = 'view'
    categories = Category.objects.all()

    if is_authenticated(request, cat_name, view_name) or is_authenticated(request, cat_name, 'create'):
        context = {'post': post, 'categories' : categories}
        return render(request, 'bulletinboard/post_detail.html', context)

    else:
        # return 권한이 없습니다 페이지 or 경고
        msg = f'{cat_name}에 접근할 권한이 없습니다.'
        messages.warning(request, msg)
        context = {'categories': categories}

        return render(request, 'landing.html', context)


def paging(post_list, kw, category, page):
    # 검색
    if kw:
        post_list = post_list.filter(
            Q(title__icontains=kw) |  # title
            Q(content__icontains=kw) |  # contents
            Q(author__name__icontains=kw) |  # post author
            Q(reply__author__name__icontains=kw)  # reply auther
        ).distinct()

    # 특정 카테고리의 post
    post_list = post_list.filter(
            Q(category__name__icontains = category))

    # 페이징처리
    paginator = Paginator(post_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    return page_obj


@login_required(login_url='common:login')
def cat_index(request, cat_name):
    """
    bulletinboard 목록 출력
    Todo:
    category view를 기본으로 설정
    상단 고정 게시물만 따로 모아서 쏴야됨
    ajax 페이징 
    """

    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    categories = Category.objects.all()  # 전체 카테고리


    # view_name
    view_name = 'view'

    # permission check
    if is_authenticated(request, cat_name, view_name) or is_authenticated(request, cat_name, 'create'):
        
        # 글 목록조회
        post_list = Post.objects.order_by('-create_date')
        
        #paging
        page_obj = paging(post_list, kw, cat_name, page)


        # fixed_on_top
        fixed_posts = post_list.filter( notice = True ) # fixed posts를 지정, 저장 가져오기

        context = {'fixed_posts' : fixed_posts, 'post_list': page_obj, 'page': page, 'kw': kw, 'categories' : categories, 'cat_name' : cat_name}

        return render(request, 'bulletinboard/post_list_cat.html', context)


    else:
        # return 권한이 없습니다 페이지 or 경고
        msg = f'{cat_name}에 접근할 권한이 없습니다.'

        messages.warning(request, msg)
        context = {'categories': categories}

        return redirect('landing')




def ajax_paging(request):
    print('cex')
    data = json.loads(request.POST.dict()['data'])

    print(data)

    page = data.get('page', '1')  # 페이지
    kw = data.get('kw', '')  # 검색어
    category = data.get('category')
    post_list = Post.objects.order_by('-create_date')
    #page_obj = paging(post_list, kw, category, page)

    #return JsonResponse({'post_list' : page_obj })
    return JsonResponse({})