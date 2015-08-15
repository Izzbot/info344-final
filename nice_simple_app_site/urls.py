from django.conf.urls import include, url
from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('nice_simple_app.urls')),
    # url(r'', include('social.apps.django_app.urls', namespace='special')),

]
