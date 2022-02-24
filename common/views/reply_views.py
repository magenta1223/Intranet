from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone

from ..forms import ReplyForm
from ..models import Wrapper, Reply
from bulletinboard.models import Category

from utils import *

@login_required(login_url='common:login')
def reply_create(request, wrapper_id):
    """
    create reply for wrapper instance
    """
    wrapper = get_object_or_404(Wrapper, pk=wrapper_id)
    categories = Category.objects.all()

    if request.method == "POST":
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.author = request.user
            reply.create_date = timezone.now()
            reply.wrapper = wrapper
            reply.save()

            # resolve_url은 인자를 받아 인자가 적용된 url을 문자열로 반환함
            # 그래서 format에 맞춰서 앞에 detail, 뒤에 answer.id가 들어가고
            # 앞서 detail에서 <a> 태그에 넣어놓은 name을 찾아서 거기로 redirect하게 된다

            return redirect('{}#reply_{}'.format(resolve_url(f'{wrapper.app_name}:detail', wrapper_id=wrapper.id), reply.id))

    else:
        form = ReplyForm()

        context = {'wrapper': wrapper, 'form': form, 'categories': categories}

        return render(request, f'{wrapper.app_name}/{wrapper.content_name}_detail.html', context)


@login_required(login_url='common:login')
def reply_modify(request, reply_id):
    """
    pybo 답변수정
    """
    reply = get_object_or_404(Reply, pk=reply_id)
    wrapper = reply.wrapper
    categories = Category.objects.all()


    if request.user != reply.author:
        messages.error(request, '수정권한이 없습니다')

        return redirect(f'{wrapper.app_name}:detail', wrapper_id=wrapper.id)


    if request.method == "POST":
        form = ReplyForm(request.POST, instance=reply)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.modify_date = timezone.now()
            reply.save()
            return redirect('{}#reply_{}'.format(resolve_url(f'{wrapper.app_name}:detail', wrapper_id=wrapper.id), reply.id))

    else:
        form = ReplyForm(instance=reply)
        context = {'reply': reply, 'form': form, 'categories' : categories}

        return render(request, 'common/reply_form.html', context)


@login_required(login_url='common:login')
def reply_delete(request, reply_id):
    """
    pybo 질문삭제
    """
    reply = get_object_or_404(Reply, pk=reply_id)
    wrapper = reply.wrapper
    if request.user != reply.author:
        messages.error(request, '삭제권한이 없습니다')
    else:
        reply.delete()

    return redirect(f'{wrapper.app_name}:detail', wrapper_id=wrapper.id)

