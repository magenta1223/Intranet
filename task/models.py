# Create your models here.
from django.db import models
from django.conf import settings
from picklefield.fields import PickledObjectField

class Estimator(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name= '작성자',on_delete=models.CASCADE, null=True) # on_delete : 계정 삭제 시 작성 질문 모두 삭제
    create_date = models.DateTimeField(verbose_name= '작성일자')
    modify_date = models.DateTimeField(verbose_name= '수정일자',null=True, blank=True)


    type = models.CharField(max_length= 30)
    name = models.CharField(max_length= 200, null=True)
    kwargs = PickledObjectField()
    additional_kwargs = PickledObjectField(null=True)
    prices = PickledObjectField(null=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = '견적서'
        verbose_name = '견적서'


class EstimatorType(models.Model):
    type = models.CharField(max_length= 30)

    def __str__(self):
        return self.type
    class Meta:
        verbose_name_plural = '품목'
        verbose_name = '품목'