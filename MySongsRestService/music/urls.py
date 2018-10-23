# music/urls.py
from django.conf.urls import url, include
from .views import ListSongsView
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    url('songs/', ListSongsView.as_view(), name="songs-all"),
    url(r'^$', ListSongsView.index, name='index')
]
urlpatterns = format_suffix_patterns(urlpatterns)
print urlpatterns