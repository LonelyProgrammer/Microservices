# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
### _ Standard Imports go here 
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import Songs
from .serializers import SongsSerializer
##This is done to test the user of our api
from django.contrib.auth.models import User

##------------
# Create your tests here.

class BaseViewTest(APITestCase):
    ##""This api test create endpoint for songs ""
    @staticmethod
    def createSongObject(title="", artist="",song_id = "",user = ""):
        if (title != "" and artist != "" and song_id == "" and user = "") :
            Songs.objects.create(song_id=song_id,title=title,artist=artist,owner=user)

    def setUp(self):
        # add test data
        user = User.objects.create(username="nerd")
        # -----Initialize client and force it to use authentication----
        self.client = APIClient()
        self.client.force_authenticate(user=user)
        ##-----------------
        self.create_song = {'song_id':'1','title':'Kathys Song', 'artist':'Simon and Gurfunkel'}
        self.createSongObject('Kathys Song','Simon and Gurfunkel',1,user)
        self.createSongObject = 
        self.response = self.client.post(
            reverse('create'),
            self.create_song,
            format="json")
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

class GetAllSongsTest(BaseViewTest):
    client = APIClient()
    def test_get_all_songs(self):
        ##"""This test ensures that all songs added in the setUp method exist when we make a GET request to the songs/ endpoint"""
        # hit the API endpoint
        expectedSong = Songs.objects.get()
        response = self.client.get(
            reverse('songs-all',
            kwargs={'pk': expectedSong.song_id}), format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #self.assertContains(response, expectedSong)

    ## Unit test to check if the authorisation is enforced    
    def test_authorization_is_enforced(self):
        """Test that the api has user authorization."""
        new_client = APIClient()
        res = new_client.get('/bucketlists/', kwargs={'pk': 2}, format="json")
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    
    def test_api_can_update_songs(self):
        ###"""Test the api can update a given bucketlist."""
        expectedSong = Songs.objects.get()
        change_song = {'song_id':'1','title': 'Winds Of Change','artist': 'Scorpions'}
        ## What does reverse actually do ?? 
        # It implements DRY(https://en.wikipedia.org/wiki/Don%27t_repeat_yourself)
        # We could just write self.client.put('/details/') 
        # but if you want to change the url in future - you'd have to update your urls.py and all references to it in your code.    
        res = self.client.put(
            reverse('songs-all', kwargs={'pk': expectedSong.song_id}),
            change_song, format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_api_can_delete_songs(self):
        ###"""Test the api can delete a bucketlist."""
        expected = Songs.objects.get()
        response = self.client.delete(
            reverse('songs-all', kwargs={'pk': expected.song_id}),
            format='json',
            follow=True)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)