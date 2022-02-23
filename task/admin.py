from django.contrib import admin

# Register your models here.
from .models import *


class ContainerAdmin(admin.ModelAdmin):
    search_fields = ['name'] # 아래 register에서 함께 들어간 model DB에서 검색이 가능해짐


    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'author':
            # setting the user from the request object
            kwargs['initial'] = request.user.id
            # making the field readonly
            kwargs['disabled'] = True
        return super().formfield_for_foreignkey(db_field, request, **kwargs)




class EstimatorTypeAdmin(admin.ModelAdmin):
    search_fields = ['subclass'] # 아래 register에서 함께 들어간 model DB에서 검색이 가능해짐



# 관리자 페이지에서 Question DB를 추가/제거 가능함
# 상품관련으로 뚝딱 가능하겠네용..

admin.site.register(EstimatorContainer, ContainerAdmin)
admin.site.register(EstimatorType, EstimatorTypeAdmin)