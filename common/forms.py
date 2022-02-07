# models
from .models import *
from django.db import models
from bulletinboard.models import Category
from django.db.models import Q
#forms
from django import forms
# fields
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.forms import ReadOnlyPasswordHashField
# etc
from django.core.exceptions import ValidationError
import datetime
from django.utils import timezone


class UserCreateForm(forms.ModelForm):
    """
    form for creating user
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    date_of_birth = forms.DateField(initial=datetime.date.today)

    class Meta:
        model = User
        fields = ('email', 'date_of_birth', 'name')  # "__all__"

    def clean_password2(self):
        """
        두 암호가 일치하는지 확인
        """
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
              raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        """
        제공된 비밀번호를 해시 형식으로 저장
        """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
              user.save()
        return user

class UserChangeForm(forms.ModelForm):
    """
    Form for updating user
    """
    password = ReadOnlyPasswordHashField()
    name = models.CharField(verbose_name='이름', max_length= 20)
    date_of_birth = models.DateField(verbose_name='생년월일', default= timezone.now)

    class Meta:
        model = User
        fields = ('name', 'email', 'date_of_birth', 'password', 'is_active', 'is_superuser')



class LevelForm(forms.ModelForm):
    """
    User를 Level에 추가하기 위한 Form
    Todo:

    Done:
    1) 저장 기능
    2) 권한설정 기능 추가
        1) 현재 존재하는 모든 catgory에 대해 permission을 자동 생성
        2) permission과 user를 할당할 수 있음
    """


    class Meta:
        model = Level
        #exclude = ['user', 'permission']
        exclude = ['user','permission']




    # Add the users field.
    users = forms.ModelMultipleChoiceField(
        queryset = User.objects.all(), # 모든 사용자를 query set에 넣고
        required = False, #필수 선택은 아님
        # Use the pretty 'filter_horizontal widget'.
        widget = FilteredSelectMultiple(verbose_name= '사용자', is_stacked= False,), # 권한 설정을 도와주는 위젯
        label = "사용자"
    )

    permissions = forms.ModelMultipleChoiceField(
        queryset = Permission.objects.all(), # 모든 사용자를 query set에 넣고
        required = False, #필수 선택은 아님
        # Use the pretty 'filter_horizontal widget'.
        widget = FilteredSelectMultiple(verbose_name ='권한', is_stacked = False), # 권한 설정을 도와주는 위젯
        label = "권한"
    )


    # m2m 일때 저장
    def __init__(self, *args, **kwargs):
        # permission update
        permissions = [f'{str(category)}_{act}' for category in Category.objects.all() for act in
                       ['create', 'view']]
        permission_set = [str(perm) for perm in Permission.objects.all()]
        # 기존 DB에 없으면 추가
        for perm in permissions:
            if perm not in permission_set:
                new_perms = Permission(permission=perm)
                new_perms.save()

        if kwargs.get('instance'):
            initial = kwargs.setdefault('initial', {})
            initial['users'] = [t.pk for t in kwargs['instance'].user_set.all()]
            initial['permissions'] = [t.pk for t in kwargs['instance'].permission.all()]
        forms.ModelForm.__init__(self, *args, **kwargs)
    def save(self, commit=True):
        instance = forms.ModelForm.save(self, False)
        old_save_m2m = self.save_m2m
        def save_m2m():
           old_save_m2m()
           instance.user_set.clear()
           instance.user_set.add(*self.cleaned_data['users'])
           instance.permission.add(*self.cleaned_data['permissions'])

        self.save_m2m = save_m2m
        if commit:
            instance.save()
            self.save_m2m()
        return instance




class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']
        labels = {
            'content': '답변내용',
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': '답변내용',
        }
