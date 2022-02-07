from django import forms
from .models import Post
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import  CKEditorUploadingWidget

class PostForm(forms.ModelForm):
    content = forms.CharField(widget = CKEditorUploadingWidget(config_name='awesome_ckeditor'))

    class Meta:
        model = Post
        fields = ['title', 'content']
