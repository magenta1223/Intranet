from django import forms
from .models import *
from common.models import User
from django.contrib.admin.widgets import FilteredSelectMultiple
# etc
from django.core.exceptions import ValidationError
import datetime
from django.utils import timezone



class VacationForm(forms.ModelForm):

    class Meta:
        model = Vacation
        fields = ['name', 'start','end', 'status', 'users', 'author']

    # Add the users field.
    users = forms.ModelMultipleChoiceField(
        queryset = User.objects.all(), # 모든 사용자를 query set에 넣고
        required = False, #필수 선택은 아님
        # Use the pretty 'filter_horizontal widget'.
        widget = FilteredSelectMultiple(verbose_name= '사용자', is_stacked= False,), # 권한 설정을 도와주는 위젯
        label = "사용자"
    )

    # m2m 일때 저장
    def __init__(self, *args, **kwargs):
        # permission update
        #permissions = [f'{str(category)}_{act}' for category in Category.objects.all() for act in
        #               ['create', 'view']]
        #permission_set = [str(perm) for perm in Permission.objects.all()]
        # 기존 DB에 없으면 추가
        #
        #for perm in permissions:
        #    if perm not in permission_set:
        #        new_perms = Permission(permission=perm)
        #        new_perms.save()

        if kwargs.get('instance'):
            initial = kwargs.setdefault('initial', {})
            initial['users'] = [t.pk for t in kwargs['instance'].user.all()]
        forms.ModelForm.__init__(self, *args, **kwargs)
    def save(self, commit=True):
        instance = forms.ModelForm.save(self, False)
        old_save_m2m = self.save_m2m
        def save_m2m():
           old_save_m2m()
           instance.user.clear()
           instance.user.add(*self.cleaned_data['users'])

        self.save_m2m = save_m2m
        if commit:
            instance.save()
            self.save_m2m()
        return instance



class TaskConfigForm(forms.ModelForm):
    class Meta:
        model = TaskConfig
        fields = ['name', 'color']



class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['start','end','signature','name', 'config', 'users', 'done', 'modify_reason']
    # Add the users field.
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),  # 모든 사용자를 query set에 넣고
        required=False,  # 필수 선택은 아님
        # Use the pretty 'filter_horizontal widget'.
        widget=FilteredSelectMultiple(verbose_name='사용자', is_stacked=False, ),  # 권한 설정을 도와주는 위젯
        label="사용자"
    )

    # m2m 일때 저장
    def __init__(self, *args, **kwargs):
        # permission update
        # permissions = [f'{str(category)}_{act}' for category in Category.objects.all() for act in
        #               ['create', 'view']]
        # permission_set = [str(perm) for perm in Permission.objects.all()]
        # 기존 DB에 없으면 추가
        #
        # for perm in permissions:
        #    if perm not in permission_set:
        #        new_perms = Permission(permission=perm)
        #        new_perms.save()

        if kwargs.get('instance'):
            initial = kwargs.setdefault('initial', {})
            initial['users'] = [t.pk for t in kwargs['instance'].user.all()]
        forms.ModelForm.__init__(self, *args, **kwargs)

    def save(self, commit=True):
        instance = forms.ModelForm.save(self, False)
        old_save_m2m = self.save_m2m

        def save_m2m():
            old_save_m2m()
            instance.user.clear()
            instance.user.add(*self.cleaned_data['users'])

        self.save_m2m = save_m2m
        if commit:
            instance.save()
            self.save_m2m()
        return instance
