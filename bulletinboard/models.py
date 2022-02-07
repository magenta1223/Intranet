from django.db import models
from django.conf import settings
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.

class Category(models.Model):
    """
    여러 게시판을 카테고리별로 관리하기 위한 기능
    Done
    1) Admin에서 관리 가능하게 -> Done!
    2) Category를 받아와서 templates/nav_cat.html을 생성하도록! -> Done!
    3) Post에 Category 주기 -> Done!
    4) Category에 맞춰서 상단바 current 설정하기 -> Done!
    5) 문자열이 아니라 선택된 값을 이용한 카테고리 생성
    """
    name = models.CharField(verbose_name= '이름', max_length=20, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        # 복수형 저장
        verbose_name_plural = '카테고리'
        verbose_name = '카테고리'


class Post(models.Model):
    """
    Post of Bulletin Board from pybo.models.Question

    Attributes:
        author : of the post
        title : of the post
        content : of the post
        create_date : of the post
        modify_date : of the post
        category : of the post

    Todo:
    관리자도 작성자, 작성일자는 수정 못하게
    """
    #
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name= '작성자',on_delete=models.CASCADE, null=True) # on_delete : 계정 삭제 시 작성 질문 모두 삭제
    create_date = models.DateTimeField(verbose_name= '작성일자')
    modify_date = models.DateTimeField(verbose_name= '수정일자', null=True, blank=True)
    title = models.CharField(verbose_name= '제목',max_length=200)
    content = RichTextUploadingField(verbose_name='내용')
    category = models.ForeignKey(Category, verbose_name= '카테고리', on_delete=models.CASCADE, null = True, blank = True)

    def __str__(self):
        return self.title

    class Meta:
        # 복수형 저장. 관리자페이지에서 이 이름으로 보인다
        verbose_name = '게시글'
        verbose_name_plural = '게시글'

# admin / 소주맥주123





