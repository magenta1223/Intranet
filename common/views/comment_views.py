from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone

from ..forms import CommentForm
from ..models import Comment, Reply
from bulletinboard.models import Category
from utils import *

@login_required(login_url='common:login')
def comment_create(request, reply_id):
    """
    create comment for wrapper class
    Todo:
    return 부분에 post, estimator 등 wrapper에 속한 개별 model말고, wrapper로 통일
    당연히 조건부 return도 사라짐
    """

    reply = get_object_or_404(Reply, pk = reply_id)
    wrapper = reply.wrapper

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            # save를 하면 원래 model인 Question이 생성
            comment = form.save(commit=False)

            comment.author = request.user
            # set time
            comment.create_date = timezone.now()
            comment.reply = reply
            comment.save()

            return redirect('{}#comment_{}'.format(resolve_url(f'{wrapper.app_name}:detail', wrapper_id=wrapper.id), comment.id))

    else:
        categories = Category.objects.all()

        form = CommentForm()
        context = {'form': form, 'categories' : categories}
        return render(request, 'common/comment_form.html', context)

# 로그인 필요, 안돼 있으면 common:login으로 안내
@login_required(login_url='common:login')
def comment_modify(request, comment_id):
    """
    pybo 질문수정
    """
    # get question from req
    comment = get_object_or_404(Comment, pk=comment_id)
    categories = Category.objects.all()
    wrapper = comment.reply.wrapper

    if request.user != comment.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect(f'{wrapper.app_name}:detail', wrapper_id= wrapper.id)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.modify_date = timezone.now()  # 수정일시 저장
            comment.save()

            return redirect('{}#comment_{}'.format(resolve_url(f'{wrapper.app_name}:detail', wrapper_id = wrapper.id), comment.id))

    else:
        form = CommentForm(instance=comment)
        context = {'form': form,'categories' : categories}
        return render(request, 'common/comment_form.html', context)

@login_required(login_url='common:login')
def comment_delete(request, comment_id):
    """
    pybo 질문삭제
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    wrapper = comment.reply.wrapper
    if request.user != comment.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect(f'{wrapper.app_name}:detail', wrapper_id= wrapper.id)
    comment.delete()

    return redirect(f'{wrapper.app_name}:detail', wrapper_id=wrapper.id)
