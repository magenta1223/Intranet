from django.contrib import admin

# Register your models here.
from .models import Post, Category

class PostAdmin(admin.ModelAdmin):
    """
    Post 관리
    삭제는 가능
    추가/변경은 불가능 : 글 쓴 사람을 맘대로 바꿀 수 있음
    """
    list_display = ('title',  'author', )
    list_filter = ('author', )
    search_fields = ('title', 'author',  )
    list_per_page = 20


    def has_delete_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        # Disable add
        return False

    def has_change_permission(self, request, obj=None):
        # Disable update
        return False

class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name'] # 아래 register에서 함께 들어간 model DB에서 검색이 가능해짐



# 관리자 페이지에서 Question DB를 추가/제거 가능함
# 상품관련으로 뚝딱 가능하겠네용..

admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)