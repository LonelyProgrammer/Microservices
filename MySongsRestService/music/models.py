# -*- coding: utf-8 -*-
from __future__ import unicode_literals

#from django.db import models
## This is added for Cassandra Support -- We will use the database as Cassandra overriding the default sql
import uuid
from cassandra.cqlengine import columns
from django_cassandra_engine.models import DjangoCassandraModel
##-------------------------------------------------
# Create your models here.
class Songs(DjangoCassandraModel):
    ## Song_id
    song_id = columns.Integer(primary_key=True)
    # song title
    title = columns.Text(required=False) ## - This is the Cassandra version
    ##title = models.CharField(max_length=255, null=False) ## - This is the sqlite version

    # name of artist or group/band
    artist = columns.Text(required=False)
    #artist = models.CharField(max_length=255, null=False)
    def __str__(self):
        ##"""Return a human readable representation of the model instance."""
        return "{} - {} - {}".format(self.song_id,self.title, self.artist)

class Owner(DjangoCassandraModel):
    ##Add an owner to this api
    owner = columns.Text(required=True)
    def __str__(self):
        ##"""Return a human readable representation of the model instance."""
        return "{}".format(self.owner)

     