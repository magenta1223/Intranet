from django.urls import path

from .views import base_views, estimator_views
from common.views import reply_views, comment_views

from django.conf.urls import include



urlpatterns = [
    # 카테고리
    path('<int:wrapper_id>/', base_views.detail, name='detail2'),


    path('download/<int:estimator_id>', estimator_views.estimator_download, name='estimator_download'),
    path('download_container/<int:container_id>', estimator_views.container_download, name='container_download'),


    path('reply/create/<int:wrapper_id>/', reply_views.reply_create, name='reply_create'),
    path('reply/modify/<int:reply_id>/', reply_views.reply_modify, name='reply_modify'),
    path('reply/delete/<int:reply_id>/', reply_views.reply_delete, name='reply_delete'),

    path('comment/create/<int:reply_id>/', comment_views.comment_create, name='comment_create'),
    path('comment/modify/<int:comment_id>/', comment_views.comment_modify, name='comment_modify'),
    path('comment/delete/<int:comment_id>/', comment_views.comment_delete, name='comment_delete'),

    path('create/', estimator_views.container_create, name='container_create'),
    path('estimator_add/', estimator_views.estimator_add, name='estimator_add'),
    path('estimator_create2/', estimator_views.estimator_create, name='estimator_create'),
    path('', base_views.multi_index, name='container_index'),
    path('multi-estimator/<int:wrapper_id>/', base_views.multi_detail, name='detail'),



]

#http://localhost:8000/bulletinboard/2/ 페이지가 요청되면
# 위 매핑 룰에 의해 http://localhost:8000/bulletinboard/<int:question_id>/가 적용되어
# question_id 에 2가 저장되고 views.detail 함수가 실행될 것이다.
# <int:question_id> 에서 int는 숫자가 매핑됨을 의미한다.

# 동일한 url name을 다른 app에서 중복으로 사용한다면?
# 아마 개망할 것
# 그래서 url name space를 의미하는 app_name이라는 변수를 꼭 지정해준다

app_name = 'task'
