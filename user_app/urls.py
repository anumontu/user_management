from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^user/(?P<id>[0-9]+)/$', views.UserProfile.as_view()),
    url(r'^user/$', views.CreateUser.as_view()),
    url(r'^users/$', views.UserList.as_view()),
    url(r'^login/$', views.Authenticate.as_view({'post': 'authenticate_user'})),
    url(r'^logout/$', views.Logout.as_view({'get': 'logout_user'})),
]
