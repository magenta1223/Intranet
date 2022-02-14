import urllib
import os
from django.http import HttpResponse, Http404
import mimetypes


def is_authenticated(request, cat_name, view_name):

    required_permission = f'{cat_name}_{view_name}'

    user_permissions = [ str(p)  for p in request.user.level.permission.all()]


    if required_permission in user_permissions or request.user.is_superuser:
        return True
    else:
        return False


def download(request, file_path, file_name):
    # local (window)
    #parent_folder = file_path.split('/')[0]

    # server (linux based server)
    parent_folder = file_path.replace(file_name, '')

    file_name = urllib.parse.quote(file_name.encode('utf-8'))
    response = HttpResponse(open(file_path, 'rb'), content_type=mimetypes.guess_type(file_path)[0])
    response['Content-Disposition'] = 'attachment;filename*=UTF-8\'\'%s' % file_name

    # 파일 정리 필요

    for f in os.listdir(parent_folder):
        if 'template' in f:
            continue
        else:
            os.remove( os.path.join(parent_folder, f) )


    return response



