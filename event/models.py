from django.db import models
from django.conf import settings
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from picklefield.fields import PickledObjectField
from colorfield.fields import ColorField
from django.db import models


class Event(models.Model):
    """
    Base
    """

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE, null = True, blank=True) # on_delete : 계정 삭제 시 작성 질문 모두 삭제
    start = models.DateTimeField(verbose_name = '시작', null = True)
    end = models.DateTimeField(verbose_name = '끝', null = True)

    create_date = models.DateTimeField(null = True,  blank=True)
    modify_date = models.DateTimeField(null = True,  blank=True)

    @property
    def is_active(self):
        now = timezone.now()
        # 비교
        return self.start < now < self.end

class VacationConfig(models.Model):
    """
    Configuration for
    """

    name = models.CharField(max_length=30)
    color = ColorField(default='#FF0000')

    def __str__(self):
        return self.name




class Vacation(Event):
    """
    vacation event
    is_active 조회, 아니면 회색
    """

    STATUS_CHOICES = (
        ('1', '신청'), # 저장값, 표시값 순서
        ('2', '승인'),
        ('3', '반려')
    )

    name = models.CharField(verbose_name='종류', max_length=30,  null = True, blank=True)
    user = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name='휴가자', blank=True) # on_delete : 계정 삭제 시 작성 질문 모두 삭제
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, null = True, blank=True)

    def __str__(self):
        return self.name

    @property
    def color(self):
        if self.is_active:
            if self.status == '1':
                return '#BDE3DD'
            elif self.status == '2':
                return '#03BD9E'
            else:
                return '#FF4040'
        else:
            return '#DCDCDC'

    class Meta:
        verbose_name = '휴가'
        verbose_name_plural = '휴가'


class TaskConfig(models.Model):
    """
    Configuration for Task
    """

    name = models.CharField(max_length=30)
    color = ColorField(default='#FF0000')

    def __str__(self):
        return self.name


class Task(Event):
    """
    사인 추가
    완료처리
    변경 가능하게 :
        > 시간 / 메모 변경
        > 변경 사유 적을 수 있게
        > 변경 이전의 status을 남겨야 함


    """

    name = models.CharField(verbose_name='종류', max_length=30)
    user = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name='휴가자', blank=True) # on_delete : 계정 삭제 시 작성 질문 모두 삭제
    config = models.ForeignKey(TaskConfig, on_delete= models.CASCADE, null = True, blank = True)
    done = models.BooleanField(default= False)

    # 변경 시, 이전 이력을 dictionary로 보관
    prev_status = PickledObjectField(null = True, blank = True)
    modify_reason = models.TextField(null = True, blank = True)
    signature = models.ImageField(null = True, blank= True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '업무'
        verbose_name_plural = '업무'