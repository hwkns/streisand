# -*- coding: utf-8 -*-

from unittest.mock import patch, ANY

from django_dynamic_fixture import G

from django.test import TestCase, RequestFactory

from profiles.models import UserProfile
from tracker.models import Swarm
from tracker.views import AnnounceView
from tracker.utils import unquote_to_hex


@patch('tracker.views.handle_announce.delay')
class AnnounceHandlerTests(TestCase):

    fixtures = ['dev.json']

    def setUp(self):
        self.factory = RequestFactory()
        self.announce_view = AnnounceView.as_view()
        self.swarm = G(Swarm, torrent_info_hash='894985f97cc25c246e37a07cd7c785993982a7cb')
        self.profile = UserProfile.objects.get(auth_key='16fd2706-8baf-433b-82eb-8c7fada847da')
        self.announce_data = {
            'info_hash': '%89I%85%F9%7C%C2%5C%24n7%A0%7C%D7%C7%85%999%82%A7%CB',
            'peer_id': '-DE1360-m8vgv0uzHUF0',
            'uploaded': '422',
            'downloaded': '381',
            'left': '0',
            'port': '1337',
        }

    def announce_request(self, announce_data):
        """
        Hack so we can use a dict with pre-urlencoded data (info_hash bytes)
        """
        params = '&'.join('='.join([k, v]) for k, v in announce_data.items())
        return self.factory.get(path='/?{params}'.format(params=params), HTTP_USER_AGENT='foobar')

    def test_announce_handler_called__proper_announce(self, handler_mock):
        request = self.announce_request(announce_data=self.announce_data)
        self.announce_view(request, auth_key=self.profile.auth_key)
        self.assertTrue(handler_mock.called)

    def test_announce_handler_called_with_correct_arguments(self, handler_mock):
        request = self.announce_request(announce_data=self.announce_data)
        self.announce_view(request, auth_key=self.profile.auth_key)
        handler_mock.assert_called_once_with(
            auth_key=self.profile.auth_key,
            info_hash=self.swarm.torrent_info_hash,
            new_bytes_uploaded=422,
            new_bytes_downloaded=381,
            bytes_remaining=0,
            event='',
            ip_address='127.0.0.1',
            port=1337,
            peer_id=unquote_to_hex('-DE1360-m8vgv0uzHUF0'),
            user_agent='foobar',
            time_stamp=ANY,
        )

    def test_announce_handler_not_called__bad_auth_key(self, handler_mock):
        request = self.announce_request(announce_data=self.announce_data)
        self.announce_view(request, auth_key='ffffffff-ffff-ffff-ffff-ffffffffffff')
        self.assertFalse(handler_mock.called)

    def test_announce_handler_not_called__bad_info_hash(self, handler_mock):
        self.announce_data.update({'info_hash': 'ffffffffffffffffffff'})
        request = self.announce_request(announce_data=self.announce_data)
        self.announce_view(request, auth_key=self.profile.auth_key)
        self.assertFalse(handler_mock.called)

    def test_announce_handler_not_called__non_compact(self, handler_mock):
        self.announce_data.update({'compact': '0'})
        request = self.announce_request(announce_data=self.announce_data)
        self.announce_view(request, auth_key=self.profile.auth_key)
        self.assertFalse(handler_mock.called)

    def test_announce_handler_not_called__non_whitelisted_peer_id(self, handler_mock):
        self.announce_data.update({'peer_id': '-FFFFFF-FFFFFFFFFFFF'})
        request = self.announce_request(announce_data=self.announce_data)
        self.announce_view(request, auth_key=self.profile.auth_key)
        self.assertFalse(handler_mock.called)

    def test_announce_handler_not_called__missing_info_hash(self, handler_mock):
        del self.announce_data['info_hash']
        request = self.announce_request(announce_data=self.announce_data)
        self.announce_view(request, auth_key=self.profile.auth_key)
        self.assertFalse(handler_mock.called)

    def test_announce_handler_not_called__missing_peer_id(self, handler_mock):
        del self.announce_data['peer_id']
        request = self.announce_request(announce_data=self.announce_data)
        self.announce_view(request, auth_key=self.profile.auth_key)
        self.assertFalse(handler_mock.called)

    def test_announce_handler_not_called__missing_port(self, handler_mock):
        del self.announce_data['port']
        request = self.announce_request(announce_data=self.announce_data)
        self.announce_view(request, auth_key=self.profile.auth_key)
        self.assertFalse(handler_mock.called)

    def test_announce_handler_not_called__missing_uploaded(self, handler_mock):
        del self.announce_data['uploaded']
        request = self.announce_request(announce_data=self.announce_data)
        self.announce_view(request, auth_key=self.profile.auth_key)
        self.assertFalse(handler_mock.called)

    def test_announce_handler_not_called__missing_downloaded(self, handler_mock):
        del self.announce_data['downloaded']
        request = self.announce_request(announce_data=self.announce_data)
        self.announce_view(request, auth_key=self.profile.auth_key)
        self.assertFalse(handler_mock.called)

    def test_announce_handler_not_called__missing_left(self, handler_mock):
        del self.announce_data['left']
        request = self.announce_request(announce_data=self.announce_data)
        self.announce_view(request, auth_key=self.profile.auth_key)
        self.assertFalse(handler_mock.called)
