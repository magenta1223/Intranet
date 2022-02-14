from django.contrib import admin

# Register your models here.
from .models import *
from common.models import User
from .forms import *

class TaskConfigAdmin(admin.ModelAdmin):
    form = TaskConfigForm



class VacationAdmin(admin.ModelAdmin):
    form = VacationForm

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        # 이미 지나간 휴가는 편집 못하게
        if obj is not None and not obj.is_active:
            return False
        return super().has_change_permission(request, obj=obj)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'author':
            # setting the user from the request object
            kwargs['initial'] = request.user.id
            # making the field readonly
            kwargs['disabled'] = True
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class TaskAdmin(admin.ModelAdmin):
    form = TaskForm
    fieldsets = (
            ('기본정보', {'fields': ( 'name', 'config', 'start', 'end', 'users')}),
            ('완료 여부', {'fields': ('done', )}),
            ('사인', {'fields': ('signature',)}),
            ('수정 이유', {'fields': ('modify_reason',)}),
    )
admin.site.register(TaskConfig, TaskConfigAdmin)
admin.site.register(Vacation, VacationAdmin)
admin.site.register(Task, TaskAdmin)