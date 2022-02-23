# Create your models here.
from django.db import models
from django.conf import settings
from picklefield.fields import PickledObjectField
from django.utils import timezone


class EstimatorContainer(models.Model):
    """
    Containter for multiple estimators
    """
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name= '작성자',on_delete=models.CASCADE, null=True) # on_delete : 계정 삭제 시 작성 질문 모두 삭제
    create_date = models.DateTimeField(verbose_name= '작성일자')
    modify_date = models.DateTimeField(verbose_name= '수정일자',null=True, blank=True)

    name = models.CharField(verbose_name = '견적서 뭉치 명', max_length= 200, null=True)

    class Meta:
        verbose_name_plural = '견적서 뭉치'
        verbose_name = '견적서 뭉치치'



class Estimator(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name= '작성자',on_delete=models.CASCADE, null=True) # on_delete : 계정 삭제 시 작성 질문 모두 삭제
    create_date = models.DateTimeField(verbose_name= '작성일자')
    modify_date = models.DateTimeField(verbose_name= '수정일자',null=True, blank=True)


    type = models.CharField(verbose_name = '품목', max_length= 30)
    name = models.CharField(verbose_name = '견적서 명', max_length= 200, null=True)
    kwargs = PickledObjectField()
    additional_kwargs = PickledObjectField(null=True)
    prices = PickledObjectField(null=True)

    container = models.ForeignKey(EstimatorContainer, on_delete = models.CASCADE, null = True, blank = True)



    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = '견적서'
        verbose_name = '견적서'

    @property
    def formatted_date(self):

        date = self.modify_date if self.modify_date is not None else self.create_date


        if timezone.now().astimezone().date() == date.astimezone().date():
            return date.astimezone().strftime('%H:%M')
        else:
            return date.astimezone().strftime('%Y-%m-%d')



class EstimatorType(models.Model):
    type = models.CharField(max_length= 30)
    name = models.CharField(max_length= 30)
    kwargs = PickledObjectField() # 각 품목별 필요한 값을 담아놓는 필드

    def __str__(self):
        return self.type
    class Meta:
        verbose_name_plural = '품목'
        verbose_name = '품목'



