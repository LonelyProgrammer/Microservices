# music/urls.py
from django.conf.urls import url, include
from .views import ListSongsView
from .views import ListDetailsAPIView
from . import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = {
    url(r'^songs/$', ListSongsView.as_view(), name="create"),
    url(r'songs/(?P<pk>[0-9]+)/$', ListDetailsAPIView.as_view(), name="songs-all"),
    url(r'^$', views.index, name='index')
}
urlpatterns = format_suffix_patterns(urlpatterns)