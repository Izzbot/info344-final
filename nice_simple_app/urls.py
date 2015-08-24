from django.conf.urls import url, patterns

from django.contrib.auth import views as auth_views

from rest_framework.urlpatterns import format_suffix_patterns

from . import views


urlpatterns = [
    url(r'^$', views.home_page, name='home_page'),
    url(r'^comparison/(?P<pk>[0-9]+)/$', views.comparison_page, name='comparison_page'),
    url(r'^comparison/new/$', views.new_comparison_page, name='new_comparison_page'),
    url(r'^about_us$', views.about_page, name='about_page'),



    # api
    url(r'^api/$', views.ApiList.as_view()),
    url(r'^api/(?P<pk>[0-9]+)/$', views.ApiDetail.as_view()),
    # url(r'^api_view$', views.api_list, name='api_list'),
    # url(r'^api_view/(?P<pk>[0-9]+)/$', views.api_url_detail.as_view(), name='api_url_detail'),

    # login via facebook
    url(r'^accounts/login/$', auth_views.login, name='login_page'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/info344final'}),
]

urlpatterns = format_suffix_patterns(urlpatterns)