import json
from copy import deepcopy

from unittest import TestCase
from unittest.mock import patch

from mvf1 import MultiViewerForF1
from mvf1 import MultiViewerForF1Error

from mvf1.mvf1_schema import mvf1_schema as schema

from sgqlc.operation import Operation

f = open('tests/players.json')
mock_players = json.load(f)
f.close()


def configure_mock_response(mock_urlopen, payload):
    if isinstance(payload, Exception):
        mock_urlopen.side_effect = payload
    else:
        mock_urlopen.return_value = payload


class TestMultiViewerForF1(TestCase):
    def setUp(self):
        self.remote = MultiViewerForF1()
        self.query = Operation(schema.Query)
        self.mutation = Operation(schema.Mutation)

    @patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
    def test_server_error(self, mock_urlopen):
        configure_mock_response(mock_urlopen,
                                {'errors': [{'message': 'Whoopsie'}]})

        with self.assertRaises(MultiViewerForF1Error):
            self.remote.live_timing_clock

    @patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
    def test_live_timing_clock(self, mock_urlopen):
        configure_mock_response(mock_urlopen,
                                {"data": {"liveTimingClock": None}})

        response = self.remote.live_timing_clock

        self.query.live_timing_clock()

        mock_urlopen.assert_called_once()
        self.assertIn("liveTimingClock", str(response))

    @patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
    def test_live_timing_state(self, mock_urlopen):
        configure_mock_response(mock_urlopen,
                                {'data': {'liveTimingState': None}})

        response = self.remote.live_timing_state

        mock_urlopen.assert_called_once()

        self.assertIn("liveTimingState", str(response))

    @patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
    def test_players(self, mock_urlopen):
        configure_mock_response(mock_urlopen,
                                mock_players)

        response = self.remote.players

        mock_urlopen.assert_called_once()

        self.assertEqual(len(response), 2)
        self.assertEqual(response[0].title, "INTERNATIONAL")

    @patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
    def test_system_info(self, mock_urlopen):
        configure_mock_response(mock_urlopen,
                                {'data': {'systemInfo': {'platform': 'linux', 'arch': 'x64'}}})

        response = self.remote.system_info

        mock_urlopen.assert_called_once()

        self.assertIn('systemInfo', str(response))

    @patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
    def test_version(self, mock_urlopen):
        configure_mock_response(mock_urlopen,
                                {'data': {'version': '1.12.6'}})

        response = self.remote.version

        mock_urlopen.assert_called_once()

        self.assertIn('version', str(response))

    @patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
    def test_player(self, mock_urlopen):
        configure_mock_response(mock_urlopen,
                                {'data': {'player':
                                          mock_players['data']['players'][0]}})

        response = self.remote.player(3)

        mock_urlopen.assert_called_once()

        self.assertEqual(response.title, "INTERNATIONAL")

    @patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
    def test_player_create(self, mock_urlopen):

        mock_urlopen.side_effect = [
            {'data': {'playerCreate': '3'}},
            {"data": {"player": mock_players['data']['players'][0]}}
        ]

        stream_data = mock_players['data']['players'][0]['streamData']

        response = self.remote.player_create(stream_data['contentId'],
                                             stream_data['channelId'])

        self.assertEqual(mock_urlopen.call_count, 2)

        self.assertEqual(response.title, "INTERNATIONAL")

    @patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
    def test_player_create_with_bounds(self, mock_urlopen):

        mock_urlopen.side_effect = [
            {'data': {'playerCreate': '3'}},
            {"data": {"player": mock_players['data']['players'][0]}}
        ]

        stream_data = mock_players['data']['players'][0]['streamData']

        response = self.remote.player_create(stream_data['contentId'],
                                             stream_data['channelId'],
                                             x=0, y=0, width=640, height=480)

        self.assertEqual(mock_urlopen.call_count, 2)

        self.assertEqual(response.title, "INTERNATIONAL")

    @patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
    def test_player_sync_to_commentary(self, mock_urlopen):

        mock_urlopen.side_effect = [
            mock_players,
            {'data': {'playerSync': True}}
        ]

        response = self.remote.player_sync_to_commentary()

        self.assertEqual(mock_urlopen.call_count, 2)

        self.assertIn('Sync', str(response))

    @patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
    def test_player_sync_to_commentary_no_commentary(self, mock_urlopen):
        altered = deepcopy(mock_players)
        altered['data']['players'][0]['streamData']['title'] = 'NOPE'

        mock_urlopen.side_effect = [
            altered,
            {'data': {'playerSync': True}}
        ]

        response = self.remote.player_sync_to_commentary()

        self.assertEqual(mock_urlopen.call_count, 1)

        self.assertIn('No player', str(response))

    @patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
    def test_player_delete(self, mock_urlopen):
        configure_mock_response(mock_urlopen,
                                {'data': {'playerDelete': True}})

        response = self.remote.player_delete(3)

        mock_urlopen.assert_called_once()

        self.assertIn('playerDelete', str(response))

    @patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
    def test_player_seek_to(self, mock_urlopen):
        configure_mock_response(mock_urlopen,
                                {'data': {'playerSeekTo': 0}})

        response = self.remote.player_seek_to(3, absolute=0)

        mock_urlopen.assert_called_once()

        self.assertIn('SeekTo', str(response))

    @patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
    def test_player_set_bounds(self, mock_urlopen):
        configure_mock_response(mock_urlopen,
                                {'data': {'playerSetBounds': {'x': 0, 'y': 0, 'width': 720, 'height': 408}}})

        response = self.remote.player_set_bounds(3, x=0, y=0)

        mock_urlopen.assert_called_once()

        self.assertIn('SetBounds', str(response))


class TestPlayer(TestCase):
    @patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
    def setUp(self, mock_urlopen):
        configure_mock_response(mock_urlopen,
                                {'data': {'player':
                                          mock_players['data']['players'][0]}})

        self.remote = MultiViewerForF1()
        self.player = self.remote.player(3)

    @patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
    def test_pause(self, mock_urlopen):
        configure_mock_response(mock_urlopen,
                                {'data': {'playerSetPaused': True}})

        response = self.player.pause()

        mock_urlopen.assert_called_once()

        self.assertIn('SetPaused', str(response))

    @patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
    def test_set_volume(self, mock_urlopen):
        configure_mock_response(mock_urlopen,
                                {'data': {'playerSetVolume': 3}})

        response = self.player.set_volume(3)

        mock_urlopen.assert_called_once()

        self.assertIn('SetVolume', str(response))

    @patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
    def test_muted(self, mock_urlopen):
        configure_mock_response(mock_urlopen,
                                {'data': {'playerSetMuted': True}})

        response = self.player.mute()

        mock_urlopen.assert_called_once()

        self.assertIn('SetMuted', str(response))

    @patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
    def test_set_fullscreen(self, mock_urlopen):
        configure_mock_response(mock_urlopen,
                                {'data': {'playerSetFullscreen': True}})

        response = self.player.set_fullscreen()

        mock_urlopen.assert_called_once()

        self.assertIn('SetFullscreen', str(response))

    @patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
    def test_set_speedometer_visibility(self, mock_urlopen):
        configure_mock_response(mock_urlopen,
                                {'data': {'playerSetSpeedometerVisibility': True}})

        response = self.player.set_speedometer_visibility()

        mock_urlopen.assert_called_once()

        self.assertIn('playerSetSpeedometerVisibility', str(response))

    @patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
    def test_sync(self, mock_urlopen):
        configure_mock_response(mock_urlopen,
                                {'data': {'playerSync': True}})

        response = self.player.sync()

        mock_urlopen.assert_called_once()

        self.assertIn('Sync', str(response))

    @patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
    def test_seek(self, mock_urlopen):
        configure_mock_response(mock_urlopen,
                                {'data': {'playerSeekTo': 0}})

        response = self.player.seek(absolute=0)

        mock_urlopen.assert_called_once()

        self.assertIn('SeekTo', str(response))

    @patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
    def test_delete(self, mock_urlopen):
        configure_mock_response(mock_urlopen,
                                {'data': {'playerDelete': True}})

        response = self.player.delete()

        mock_urlopen.assert_called_once()

        self.assertIn('Delete', str(response))

    @patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
    def test_set_bounds(self, mock_urlopen):
        configure_mock_response(mock_urlopen,
                                {'data': {'playerSetBounds': True}})

        response = self.player.set_bounds(x=0, y=0)

        mock_urlopen.assert_called_once()

        self.assertIn('SetBounds', str(response))

    @patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
    def test_switch_stream(self, mock_urlopen):

        mock_urlopen.side_effect = [
            {'data': {'playerDelete': True}},
            {'data': {'playerCreate': '3'}},
            {"data": {"player": mock_players['data']['players'][0]}}
        ]

        response = self.player.switch_stream('INTERNATIONAL')

        self.assertEqual(mock_urlopen.call_count, 3)

        self.assertEqual(response.title, "INTERNATIONAL")
