from rest_framework import serializers
from .models import Songs


class SongsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Songs
        fields = ("song_id","title", "artist")