from django.urls import path
from .views import base_views, post_views

from common.views import reply_views, comment_views
from django.conf.urls import include

urlpatterns = [
    # 카테고리
    path('<int:wrapper_id>/', base_views.detail, name='detail'), # 순서 바꾸면 안됨. 기본적으로 문자로 인식해서 cat_index로 들어가버림
    path('<str:cat_name>/', base_views.cat_index, name='cat_index'),

    path('post/create/', post_views.post_create, name='post_create'),
    path('post/modify/<int:post_id>/', post_views.post_modify, name='post_modify'),
    path('post/delete/<int:post_id>/', post_views.post_delete, name='post_delete'),

    path('reply/create/<int:wrapper_id>/', reply_views.reply_create, name='reply_create'),
    path('reply/modify/<int:reply_id>/', reply_views.reply_modify, name='reply_modify'),
    path('reply/delete/<int:reply_id>/', reply_views.reply_delete, name='reply_delete'),

    path('comment/create/<int:reply_id>/', comment_views.comment_create, name='comment_create'),
    path('comment/modify/<int:comment_id>/', comment_views.comment_modify, name='comment_modify'),
    path('comment/delete/<int:comment_id>/', comment_views.comment_delete, name='comment_delete'),

]

#http://localhost:8000/bulletinboard/2/ 페이지가 요청되면
# 위 매핑 룰에 의해 http://localhost:8000/bulletinboard/<int:question_id>/가 적용되어
# question_id 에 2가 저장되고 views.detail 함수가 실행될 것이다.
# <int:question_id> 에서 int는 숫자가 매핑됨을 의미한다.

# 동일한 url name을 다른 app에서 중복으로 사용한다면?
# 아마 개망할 것
# 그래서 url name space를 의미하는 app_name이라는 변수를 꼭 지정해준다

app_name = 'bulletinboard'