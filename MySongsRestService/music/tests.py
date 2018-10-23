# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
### _ Standard Imports go here 
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import Songs
from .serializers import SongsSerializer

##------------
# Create your tests here.
class BaseViewTest(APITestCase):
    ##""This api test create endpoint for songs ""
    client = APIClient()

    @staticmethod
    def create_song(title="", artist="",song_id = ""):
        if title != "" and artist != "" and song_id == "" :
            Songs.objects.create(song_id = song_id,title=title, artist=artist)

    def setUp(self):
        # add test data
        self.create_song(1,"like glue", "sean paul")
        # self.create_song(2,"simple song", "konshens")
        # self.create_song(3,"love is wicked", "brick and lace")
        # self.create_song(4,"jam rock", "damien marley")

class GetAllSongsTest(BaseViewTest):

    def test_get_all_songs(self):
        ##"""This test ensures that all songs added in the setUp method exist when we make a GET request to the songs/ endpoint"""
        # hit the API endpoint
        response = self.client.get(
            reverse("songs-all", kwargs={"version": "v1"})
        )
        # fetch the data from db
        expected = Songs.objects.all()
        serialized = SongsSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_api_can_update_songs(self):
        ###"""Test the api can update a given bucketlist."""
        expected = Songs.objects.get()
        change_song = {'title': 'This is awesome'}
        res = self.client.put(
            reverse('details', kwargs={"version": "v1"}),
            change_song, format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_api_can_delete_songs(self):
        ###"""Test the api can delete a bucketlist."""
        expected = Songs.objects.get()
        response = self.client.delete(
            reverse('details', kwargs={'pk': expected.id}),
            format='json',
            follow=True)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)