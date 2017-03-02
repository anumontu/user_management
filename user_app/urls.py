from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^user/(?P<user_id>[0-9]+)/$', views.UserProfile.as_view({'get': 'get_user', 'put': 'update_user'})),
    url(r'^user/$', views.CreateUser.as_view({'post': 'create_user'})),
    url(r'^login/$', views.Authenticate.as_view({'post': 'authenticate_user'})),
    url(r'^logout/$', views.Logout.as_view({'get': 'logout_user'})),
]
