from rest_framework import serializers
from .models import Songs
from django_cassandra_engine.rest import serializers

class SongsSerializer(serializers.DjangoCassandraModelSerializer):
    class Meta:
        model = Songs
        fields = ("song_id","title", "artist")