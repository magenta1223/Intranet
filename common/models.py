from django.db import models
from django.db.models import Q
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils import timezone
from bulletinboard.models import *
from task.models import *
from django.conf import settings



class Permission(models.Model):
    """
    permission
    Todo:

    Done:
    https://www.geeksforgeeks.org/python-user-groups-custom-permissions-django/
    현재 bulletinboard의 모든 category에 대해 생성,
    """
    permission = models.CharField(max_length=50)
    def __str__(self):
        return self.permission
    class Meta:
        verbose_name_plural = '권한'
        verbose_name = '권한'

class Level(models.Model):
    """
    User의 그룹이 됨
    Todo:

    Done:
    1) multiplechoice fields 구현
    2) 저장기능
    3) permission과 manytomany로 연결

    """

    level = models.CharField(verbose_name='직급', max_length= 20, unique= True)
    permission = models.ManyToManyField(Permission, verbose_name='권한',related_name= 'perms')

    def __str__(self):
        return self.level
    class Meta:
        verbose_name_plural = '직급'
        verbose_name = '직급'




class UserManager(BaseUserManager):
    def create_user(self, email, date_of_birth, name, password=None):
        """지정된 email, data_of_birth로 사용자를 생성하고 저장한다."""
        if not email:
            # 사용자 email이 없을때
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            date_of_birth = date_of_birth,
            name = name,
        )

        levels = Level.objects.all()
        level = levels.filter(
            Q(level__icontains='Dummy')).distinct()[0]
        user.level = level
        user.set_password(password)
        user.create_date = timezone.now()

        user.save(using=self._db)


        return user

    def create_superuser(self, email, date_of_birth, name, password=None):
        """
        create superuser

        Todo:

        Done:


        """
        if not len(Level.objects.all()):

            level = Level(level='Dummy')
            level.save()
            level = Level(level='Admin')
            level.save()
        else:
            levels = Level.objects.all()
            level = levels.filter(
                Q(level__icontains='Admin')).distinct()[0]
        user = self.create_user(
            email,
            password=password,
            date_of_birth = date_of_birth,
            name = name,
        )
        user.level = level
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    """
    Todo :
    지금은 permission의 역할을 하는 model을 따로 만들어서 하고 있음
    내장 기능으로 변환 필요

    Done :
    1) assign level
    2) no change by superuser except level / permission / is_active

    """

    email = models.EmailField(verbose_name='이메일 주소 / ID', max_length=255, unique=True)
    name = models.CharField(verbose_name='이름', max_length= 20)
    date_of_birth = models.DateField(verbose_name='생년월일', default= timezone.now)
    is_active = models.BooleanField(verbose_name='활성화', default=False)
    is_superuser = models.BooleanField(verbose_name='관리자',default=False)
    level = models.ForeignKey(Level, verbose_name='직급', on_delete=models.CASCADE, null=True)
    create_date = models.DateTimeField(verbose_name='생성일자', null = True,  blank=True) # verbose_name='생성일자'
    modify_date = models.DateTimeField(verbose_name='수정일자', null=True, blank=True) # verbose_name='수정일자',

    #profile_image = models.ImageField(width_field= 300, height_field= 300, null=True, blank=True, upload_to= "profile-image")

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth', 'name']

    def __str__(self):
        return f'{self.name} ({self.email})'

    def has_perm(self, perm, obj=None):
        """사용자에게 특정 권한이 있는지 확인"""
        return True

    def has_module_perms(self, app_label):
        """사용자가 app_label 앱을 볼 수 있는 권한이 있는지 확인"""
        return True

    @property
    def is_staff(self):
        """User가 관리자인지 확인"""
        return self.is_superuser

    class Meta:
        verbose_name_plural = '사용자'
        verbose_name = '사용자'


class Wrapper(models.Model):
    """
    contents wrapper
    """
    post = models.OneToOneField(Post, on_delete=models.CASCADE, null = True)
    estimator = models.OneToOneField(Estimator, on_delete=models.CASCADE, null = True)

    app_name = models.CharField(max_length= 30)
    content_name = models.CharField(max_length= 30)

    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name= '작성자',on_delete=models.CASCADE, null=True) # on_delete : 계정 삭제 시 작성 질문 모두 삭제
    create_date = models.DateTimeField(verbose_name= '작성일자')
    modify_date = models.DateTimeField(verbose_name= '수정일자',null=True, blank=True)


class Reply(models.Model):
    """
    Reply of the Bulletin Board's post from pybo.models.Answer

    Attributes:
        wrapper : upper model for contents wrapping
        author : of the reply
        content : of the reply
        create_date : of the reply
        modify_date : of the reply
    """
    wrapper = models.ForeignKey(Wrapper, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    content = models.TextField()
    create_date = models.DateTimeField(verbose_name= '작성일자')
    modify_date = models.DateTimeField(verbose_name= '수정일자', null=True, blank=True)

class Comment(models.Model):
    """
    Comment for Reply in the Bulletin Board's post from pybo.models.Comment

    Attributes:
        author : of the reply
        content : of the reply
        create_date : of the reply
        modify_date : of the reply
    """
    reply = models.ForeignKey(Reply, null=True, blank=True, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField(verbose_name= '작성일자')
    modify_date = models.DateTimeField(verbose_name= '수정일자', null=True, blank=True)