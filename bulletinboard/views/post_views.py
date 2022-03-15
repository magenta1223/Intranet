from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db.models import Q

from ..forms import PostForm
from ..models import Post, Category
from common.models import Wrapper
from utils import *


@login_required(login_url='common:login')
def post_create(request, category = None):
    """
    create post

    Todo:

    Done:
    1) request의 category 를 가져와서 post의 category에 집어넣자. -> Done!
    """
    view_name = 'create'

    if request.method == 'POST':
        # submit modified one
        # POST를 parameter로 넣으면
        # QuestionForm에서 정의한 field에 POST의 값을 사용한다
        form = PostForm(request.POST)

        if form.is_valid():
            cat_name = request.POST.get('category')

            if is_authenticated(request, cat_name, view_name):
                post = form.save(commit=False)
                post.author = request.user
                post.category = Category.objects.all().filter(
                    Q(name__icontains=cat_name)
                ).distinct()[0]

                # set time
                print(request.POST['notice'])

                post.notice = bool(request.POST['notice'])

                post.create_date = timezone.now()
                post.save()

                wrapper = Wrapper(post = post, author = post.author, create_date = post.create_date, app_name = 'bulletinboard', content_name = 'post')
                wrapper.save()
                return redirect('bulletinboard:cat_index', cat_name = cat_name)

            else:
                msg = f'{cat_name}에 게시글을 생성할 권한이 없습니다.'
                messages.warning(request, msg)
                # 다시 돌아감
                form = PostForm()
                categories = Category.objects.all()
                context = {'form': form, 'categories': categories}
                return render(request, 'bulletinboard/post_form.html', context)

    else:
        # 처음 접근 시, GET을 사용 (링크를 통한 페이지 요청의 경우 GET을 사용한다)
        form = PostForm()
        categories = Category.objects.all()
        context = {'form': form, 'categories' : categories, 'category' : category}
        return render(request, 'bulletinboard/post_form.html', context)

# 로그인 필요, 안돼 있으면 common:login으로 안내
@login_required(login_url='common:login')
def post_modify(request, post_id):
    """
    modify post

    Todo:

    Done:
    1) category 수정
    """
    # get question from req
    post = get_object_or_404(Post, pk=post_id)
    wrapper = post.wrapper

    # user verification
    if request.user != post.author:
        messages.error(request, '수정권한이 없습니다.')
        return redirect('bulletinboard:detail', wrapper_id=wrapper.id)

    # submit modified
    if request.method == "POST":
        # get form
        form = PostForm(request.POST, instance=post)

        # get category
        cat_name = request.POST.get('category')
        categories = Category.objects.all().filter(
            Q(name__icontains=cat_name)).distinct()

        post.category = categories[0]

        if form.is_valid():
            post = form.save(commit=False)
            post.modify_date = timezone.now()  # 수정일시 저장
            post.save()
            return redirect('bulletinboard:detail', wrapper_id=wrapper.id)
    else:
        form = PostForm(instance=post)
        categories = Category.objects.all()
    

    context = {'form': form, 'categories' : categories, 'category' : post.category}

    return render(request, 'bulletinboard/post_form.html', context)

@login_required(login_url='common:login')
def post_delete(request, post_id):
    """
    delete post

    Todo:

    Done:
    """
    post = get_object_or_404(Post, pk=post_id)
    wrapper = post.wrapper
    if request.user != post.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('bulletinboard:detail', wrapper_id=wrapper.id)
    cat_name = str(post.category)
    post.delete()

    return redirect('bulletinboard:cat_index', cat_name = cat_name)