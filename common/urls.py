from django.urls import path
from django.contrib.auth import views as auth_views

from .views import custom_auth, profile_views
from event.views import event_views


app_name = 'common'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', custom_auth.signup, name='signup'),
    path('profile/', profile_views.profile, name='profile'),
    path('profile/modify', profile_views.profile_modify, name='profile_modify'),
    path('profile/schedule/', event_views.calendar_view, name='myschedule'),
    path('profile/request', event_views.vacation_request, name='vacation_request'),
    path('profile/test', event_views.test, name='test'),

]