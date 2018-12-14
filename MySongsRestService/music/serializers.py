from rest_framework import serializers
from .models import Songs
from django_cassandra_engine.rest import serializers

class SongsSerializer(serializers.DjangoCassandraModelSerializer):
    ## We have made this readonly so that the users cannot modify this
    owner = serializers.ReadOnlyField(source='owner.username') # ADD THIS LINE
    class Meta:
        model = Songs
        fields = ("song_id","title", "artist","owner")