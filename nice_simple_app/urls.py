from django.conf.urls import url, patterns
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^$', views.home_list, name='home_list'),
]

urlpatterns = format_suffix_patterns(urlpatterns)