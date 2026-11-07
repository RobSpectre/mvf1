import json
from unittest import TestCase
from unittest.mock import patch

import pytest
from fastmcp import Client
from fastmcp.exceptions import ToolError

from mvf1 import MultiViewerForF1, MultiViewerForF1Error, Player
from mvf1.mcp import create_mcp_server
from mvf1.mvf1_schema import AlwaysOnTopLevel


SUBSCRIPTIONS = {'data': {'activeSubscriptions': [{
    'subscriptionType': 'F1TV_PREMIUM',
    'expiresAt': None,
    'signature': 'test-signature',
}]}}
SUBSCRIPTIONS_QUERY = (
    'query {\n  activeSubscriptions {\n'
    '    subscriptionType\n    expiresAt\n    signature\n  }\n}'
)


class TestApiControls(TestCase):
    def setUp(self):
        self.remote = MultiViewerForF1()
        with open('tests/players.json') as fixture:
            self.player = Player(json.load(fixture)['data']['players'][0])

    @patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
    def test_active_subscriptions(self, endpoint):
        for payload in (SUBSCRIPTIONS, {'data': {'activeSubscriptions': []}}):
            with self.subTest(payload=payload):
                endpoint.reset_mock()
                endpoint.return_value = payload
                self.assertEqual(self.remote.active_subscriptions, payload)
                endpoint.assert_called_once()
                self.assertEqual(str(endpoint.call_args.args[0]), SUBSCRIPTIONS_QUERY)

    @patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
    def test_active_subscriptions_error(self, endpoint):
        endpoint.return_value = {'errors': [{'message': 'Unavailable'}]}
        with self.assertRaisesRegex(MultiViewerForF1Error, 'Unavailable'):
            self.remote.active_subscriptions

    @patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
    def test_create_by_channel_id(self, endpoint):
        endpoint.return_value = {'data': {'playerCreate': '3'}}
        for content_id in ('1000001067', 1000001067):
            for channel_id in (0, 42):
                with self.subTest(content_id=content_id, channel_id=channel_id):
                    self.assertEqual(
                        self.remote.player_create(content_id, channel_id=channel_id),
                        endpoint.return_value,
                    )
                    query = str(endpoint.call_args.args[0])
                    self.assertIn('contentId: "1000001067"', query)
                    self.assertIn(f'channelId: {channel_id}', query)

        # Existing positional stream selectors keep their meaning.
        self.remote.player_create('1000001067', 'HAM')
        query = str(endpoint.call_args.args[0])
        self.assertIn('driverTla: "HAM"', query)
        self.assertNotIn('channelId:', query)

    @patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
    def test_always_on_top_levels(self, endpoint):
        endpoint.return_value = {'data': {'playerSetAlwaysOnTop': True}}
        for level in AlwaysOnTopLevel.__choices__:
            with self.subTest(level=level):
                for call in (
                    lambda: self.remote.player_set_always_on_top(3, False, level),
                    lambda: self.player.set_always_on_top(False, level),
                ):
                    self.assertEqual(call(), endpoint.return_value)
                    query = str(endpoint.call_args.args[0])
                    self.assertIn('alwaysOnTop: false', query)
                    self.assertIn(f'level: {level}', query)

        self.remote.player_set_always_on_top(3)
        self.assertNotIn('level:', str(endpoint.call_args.args[0]))

    @patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
    def test_invalid_level(self, endpoint):
        with self.assertRaisesRegex(MultiViewerForF1Error, 'Invalid always-on-top'):
            self.remote.player_set_always_on_top(3, True, 'NOT_A_LEVEL')
        endpoint.assert_not_called()

    @patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
    def test_fractional_seek_and_volume(self, endpoint):
        for position in ({'absolute': 12.75}, {'relative': -0.25}):
            endpoint.return_value = {'data': {'playerSeekTo': 12.75}}
            for call in (
                lambda: self.remote.player_seek_to(3, **position),
                lambda: self.player.seek(**position),
            ):
                self.assertEqual(call(), endpoint.return_value)
                key, value = next(iter(position.items()))
                self.assertIn(f'{key}: {value}', str(endpoint.call_args.args[0]))

        for volume in (0, 37.5, 150.25):
            endpoint.return_value = {'data': {'playerSetVolume': volume}}
            for call in (
                lambda: self.remote.player_set_volume(3, volume),
                lambda: self.player.set_volume(volume),
            ):
                self.assertEqual(call(), endpoint.return_value)
                self.assertIn(f'volume: {float(volume)}', str(endpoint.call_args.args[0]))


@pytest.mark.asyncio
@pytest.mark.parametrize('subscriptions', [SUBSCRIPTIONS, {'data': {'activeSubscriptions': []}}])
@patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
async def test_mcp_active_subscriptions(endpoint, subscriptions):
    endpoint.return_value = subscriptions
    async with Client(create_mcp_server()) as client:
        response = await client.call_tool('active_subscriptions')
    assert response.data == subscriptions
    assert str(endpoint.call_args.args[0]) == SUBSCRIPTIONS_QUERY


@pytest.mark.asyncio
@pytest.mark.parametrize('content_id', ['1000001067', 1000001067])
@patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
async def test_mcp_create_by_channel_id(endpoint, content_id):
    endpoint.return_value = {'data': {'playerCreate': '3'}}
    async with Client(create_mcp_server()) as client:
        response = await client.call_tool('player_create', {
            'content_id': content_id, 'channel_id': 0,
        })
    assert response.data == endpoint.return_value
    query = str(endpoint.call_args.args[0])
    assert 'contentId: "1000001067"' in query
    assert 'channelId: 0' in query


@pytest.mark.asyncio
@pytest.mark.parametrize('tool,arguments,field,expected', [
    ('player_seek_to', {'absolute': 12.75}, 'playerSeekTo', 'absolute: 12.75'),
    ('player_seek_to', {'relative': -0.25}, 'playerSeekTo', 'relative: -0.25'),
    ('player_set_volume', {'volume': 37.5}, 'playerSetVolume', 'volume: 37.5'),
    ('player_set_volume', {'volume': 150.25}, 'playerSetVolume', 'volume: 150.25'),
    ('player_set_always_on_top', {'always_on_top': True, 'level': 'FLOATING'},
     'playerSetAlwaysOnTop', 'level: FLOATING'),
    ('player_set_always_on_top', {'always_on_top': False, 'level': 'STATUS'},
     'playerSetAlwaysOnTop', 'level: STATUS'),
])
@patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
async def test_mcp_control_arguments(endpoint, tool, arguments, field, expected):
    endpoint.return_value = {'data': {field: True}}
    async with Client(create_mcp_server()) as client:
        response = await client.call_tool(tool, {'id': 3, **arguments})
    assert response.data == endpoint.return_value
    endpoint.assert_called_once()
    assert expected in str(endpoint.call_args.args[0])


@pytest.mark.asyncio
@patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
async def test_mcp_invalid_level(endpoint):
    async with Client(create_mcp_server()) as client:
        with pytest.raises(ToolError, match='Invalid always-on-top'):
            await client.call_tool('player_set_always_on_top', {
                'id': 3, 'level': 'NOT_A_LEVEL',
            })
    endpoint.assert_not_called()
