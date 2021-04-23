from rest_framework.test import APIClient
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from channel.models import Channel
from User.models import ConsultantProfile

# SEARCH_CHANNEL = reverse()
class PublicSearchForChannelTests(TestCase):
    """Test unauthenticated recipe API access"""
    def setUp(self):
        
        self.client = APIClient()
        consultant1=ConsultantProfile.objects.create(username="test", phone_number="09184576125", first_name="hossein", last_name="masoudi", email="test1@gmailcom", password="qwertyu", certificate="111", user_type='Immigration')
        ch1=Channel.objects.create(name="Test",description= "immegrate to UK", invite_link='test-link', consultant=consultant1)        
        consultant2=ConsultantProfile.objects.create(username="alialipour", phone_number="09184526798", first_name="ali", last_name="alipour", email="test2@gmailcom", password="bvcxz", certificate="3333", user_type='Psychology')
        ch2=Channel.objects.create(name="lawery",description= "join and win the Court", invite_link='UK-Imagrate', consultant=consultant2)
        consultant3=ConsultantProfile.objects.create(username="amin", phone_number="09185762564", first_name="amini", last_name="masoudpour", email="amin@gmailcom", password="09876509ll", certificate="2586", user_type='Immigration')
        ch3=Channel.objects.create(name="Test",description= "immegrate to Germany", invite_link='Immigrate-Germany', consultant=consultant3)        


    def test_get_all_object_in_category(self):
        """ test when query is set to '' => output is all object in category """
        res = self.client.get('/channel/search-for-channel/?query=&search_category=Immigration')
        print(res.status_code)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['data']), 2)
    def test_check_search_in_channel_name(self):
        """ check search in   """