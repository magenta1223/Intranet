from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Level, Permission
from .forms import UserCreateForm, UserChangeForm, LevelForm

class UserAdmin(UserAdmin):
    """사용자 인스턴스를 추가하고 변경하는 양식"""
    form = UserChangeForm
    add_form = UserCreateForm

    # 사용자 모델을 표시하는데 사용할 필드
    list_display = ('email', 'name', 'date_of_birth', 'is_superuser',)
    list_filter = ('is_superuser',)
    fieldsets = (
            (None, {'fields': ('email', 'password')}),
            ('계정 정보', {'fields': ('name', 'date_of_birth', 'level', 'create_date')}),
            ('계정 활성화', {'fields': ('is_active',)}),
    )

    add_fieldsets = (
            (None, {
              'classes': ('wide',),
              'fields': ('email', 'password1', 'password2',),
        }),
    )
    search_fields = ('email','name')
    ordering = ('email',)
    filter_horizontal = ()


class LevelAdmin(admin.ModelAdmin):
    form = LevelForm
    #filter_horizontal = ['permission']
    #search_fields = ['level'] # 아래 register에서 함께 들어간 model DB에서 검색이 가능해짐
    class Media:
        js = ('ckeditor.js',)

# 새 UserAdmin을 등록하기
admin.site.register(User, UserAdmin)
admin.site.register(Level, LevelAdmin)

