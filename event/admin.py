from django.contrib import admin

# Register your models here.
from .models import *
from .forms import *

class TaskConfigAdmin(admin.ModelAdmin):
    form = TaskConfigForm

class VacationAdmin(admin.ModelAdmin):
    form = VacationForm

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return True

class TaskAdmin(admin.ModelAdmin):
    form = TaskForm

admin.site.register(TaskConfig, TaskConfigAdmin)
admin.site.register(Vacation, VacationAdmin)
admin.site.register(Task, TaskAdmin)