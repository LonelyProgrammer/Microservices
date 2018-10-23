# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from rest_framework import generics
from .models import Songs
from .serializers import SongsSerializer

 ##This is for Cassandra
from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from cassandra.cluster import Cluster

class ListSongsView(generics.ListAPIView):
    ##"""Provides a get method handler."""
    queryset = Songs.objects.all()
    serializer_class = SongsSerializer
    ## Cassandra Insert -- Normally for sqlite we can use serializer.save() for Saving POST data
    def index(self, serializer):
        cluster = Cluster(['127.0.0.1'])
        session = cluster.connect()
        session.set_keyspace('db')
        insert = Songs(song_id = serializer.song_id,title=serializer.title, artist=serializer.artist)
        insert.save()
        cluster.shutdown()