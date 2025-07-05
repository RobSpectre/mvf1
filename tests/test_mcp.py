import json
import pytest
from unittest.mock import patch

from fastmcp import Client
from mvf1.mcp import mcp


with open('tests/players.json') as f:
    mock_players = json.load(f)


def configure_mock_response(mock_urlopen, payload):
    if isinstance(payload, Exception):
        mock_urlopen.side_effect = payload
    else:
        mock_urlopen.return_value = payload


@pytest.mark.asyncio
@patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
async def test_f1_live_timing_clock(mock_urlopen):
    async with Client(mcp) as client:
        configure_mock_response(mock_urlopen,
                                {"data": {"liveTimingClock": None}})
        response = await client.call_tool('f1_live_timing_clock')
        mock_urlopen.assert_called_once()
        assert "liveTimingClock" in str(response)


@pytest.mark.asyncio
@patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
async def test_f1_live_timing_state(mock_urlopen):
    async with Client(mcp) as client:
        configure_mock_response(mock_urlopen,
                                {'data': {'liveTimingState': None}})
        response = await client.call_tool('f1_live_timing_state')
        mock_urlopen.assert_called_once()
        assert "liveTimingState" in str(response)


@pytest.mark.asyncio
@patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
async def test_fiawec_live_timing_state(mock_urlopen):
    async with Client(mcp) as client:
        configure_mock_response(mock_urlopen,
                                {'data': {'liveTimingState': None}})
        response = await client.call_tool("fiawec_live_timing_state")
        mock_urlopen.assert_called_once()
        assert "liveTimingState" in str(response)


@pytest.mark.asyncio
@patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
async def test_players(mock_urlopen):
    async with Client(mcp) as client:
        configure_mock_response(mock_urlopen,
                                mock_players)
        response = await client.call_tool("players")
        mock_urlopen.assert_called_once()
        response_str = str(response)
        assert "INTERNATIONAL" in response_str
        assert "3:" in response_str  # Check for expected player format


@pytest.mark.asyncio
@patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
async def test_system_info(mock_urlopen):
    async with Client(mcp) as client:
        configure_mock_response(mock_urlopen,
                                {'data':
                                    {'systemInfo':
                                        {'platform': 'linux', 'arch': 'x64'}}})
        response = await client.call_tool("system_info")
        mock_urlopen.assert_called_once()
        assert 'systemInfo' in str(response)


@pytest.mark.asyncio
@patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
async def test_version(mock_urlopen):
    async with Client(mcp) as client:
        configure_mock_response(mock_urlopen,
                                {'data': {'version': '1.12.6'}})
        response = await client.call_tool("version")
        mock_urlopen.assert_called_once()
        assert 'version' in str(response)


@pytest.mark.asyncio
@patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
async def test_player(mock_urlopen):
    async with Client(mcp) as client:
        configure_mock_response(mock_urlopen,
                                {'data':
                                    {'player':
                                        mock_players['data']['players'][0]}})
        response = await client.call_tool("player", {"id": 3})
        mock_urlopen.assert_called_once()
        assert "INTERNATIONAL" in str(response)


@pytest.mark.asyncio
@patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
async def test_player_create(mock_urlopen):
    async with Client(mcp) as client:
        configure_mock_response(mock_urlopen,
                                {'data': {'playerCreate': '3'}})
        stream_data = mock_players['data']['players'][0]['streamData']
        response = await client.call_tool("player_create",
                                          {"content_id":
                                              stream_data['contentId']})
        assert mock_urlopen.call_count == 1
        assert "playerCreate" in str(response)


@pytest.mark.asyncio
@patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
async def test_player_create_with_bounds(mock_urlopen):
    async with Client(mcp) as client:
        configure_mock_response(mock_urlopen,
                                {'data': {'playerCreate': '3'}})
        stream_data = mock_players['data']['players'][0]['streamData']
        response = await client.call_tool("player_create",
                                          {"content_id":
                                              stream_data['contentId'],
                                           "x": 0,
                                           "y": 0,
                                           "width": 640,
                                           "height": 480})
        assert mock_urlopen.call_count == 1
        assert "playerCreate" in str(response)


@pytest.mark.asyncio
@patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
async def test_player_sync_to_commentary(mock_urlopen):
    async with Client(mcp) as client:
        mock_urlopen.side_effect = [
            mock_players,
            {'data': {'playerSync': True}}
        ]
        response = await client.call_tool("player_sync_to_commentary")
        assert mock_urlopen.call_count == 2
        assert 'Sync' in str(response)


@pytest.mark.asyncio
@patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
async def test_player_delete(mock_urlopen):
    async with Client(mcp) as client:
        configure_mock_response(mock_urlopen,
                                {'data': {'playerDelete': True}})
        response = await client.call_tool("player_delete",
                                          {"id": 3})

        mock_urlopen.assert_called_once()
        assert 'playerDelete' in str(response)


@pytest.mark.asyncio
@patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
async def test_player_seek_to(mock_urlopen):
    async with Client(mcp) as client:
        configure_mock_response(mock_urlopen,
                                {'data': {'playerSeekTo': 0}})
        response = await client.call_tool("player_seek_to",
                                          {"id": 3,
                                           "absolute": 0})
        mock_urlopen.assert_called_once()
        assert 'SeekTo' in str(response)


@pytest.mark.asyncio
@patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
async def test_player_set_bounds(mock_urlopen):
    async with Client(mcp) as client:
        configure_mock_response(mock_urlopen,
                                {'data':
                                    {'playerSetBounds':
                                        {'x': 0,
                                         'y': 0,
                                         'width': 720,
                                         'height': 408}}})
        response = await client.call_tool("player_set_bounds",
                                          {"id": 3,
                                           "x": 0,
                                           "y": 0})
        mock_urlopen.assert_called_once()
        assert 'SetBounds' in str(response)


@pytest.mark.asyncio
@patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
async def test_player_set_always_on_top(mock_urlopen):
    async with Client(mcp) as client:
        configure_mock_response(mock_urlopen,
                                {'data': {'playerAlwaysOnTop': True}})
        response = await client.call_tool("player_set_always_on_top",
                                          {"id": 3})
        mock_urlopen.assert_called_once()
        assert 'AlwaysOnTop' in str(response)


@pytest.mark.asyncio
@patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
async def test_player_set_driver_header_mode(mock_urlopen):
    async with Client(mcp) as client:
        configure_mock_response(mock_urlopen,
                                {'data':
                                    {'playerSetDriverHeaderMode':
                                        'OBC_LIVE_TIMING'}})
        response = await client.call_tool("player_set_driver_header_mode",
                                          {"id": 3,
                                           "mode": "OBC_LIVE_TIMING"})

        mock_urlopen.assert_called_once()
        assert 'OBC_LIVE_TIMING' in str(response)

@pytest.mark.asyncio
@patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
async def test_player_set_volume(mock_urlopen):
    async with Client(mcp) as client:
        configure_mock_response(mock_urlopen,
                                {'data': {'playerVolume': 0}})
        response = await client.call_tool("player_set_volume",
                                          {"id": 3,
                                           "volume": 0})
        mock_urlopen.assert_called_once()
        assert 'Volume' in str(response)


@pytest.mark.asyncio
@patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
async def test_player_set_paused(mock_urlopen):
    async with Client(mcp) as client:
        configure_mock_response(mock_urlopen,
                                {'data': {'playerPaused': True}})
        response = await client.call_tool("player_set_paused",
                                          {"id": 3,
                                           "paused": True})
        mock_urlopen.assert_called_once()
        assert 'Paused' in str(response)


@pytest.mark.asyncio
@patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
async def test_player_set_fullscreen(mock_urlopen):
    async with Client(mcp) as client:
        configure_mock_response(mock_urlopen,
                                {'data': {'playerFullscreen': True}})
        response = await client.call_tool("player_set_fullscreen",
                                          {"id": 3,
                                           "fullscreen": True})
        mock_urlopen.assert_called_once()
        assert 'Fullscreen' in str(response)


@pytest.mark.asyncio
@patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
async def test_player_set_muted(mock_urlopen):
    async with Client(mcp) as client:
        configure_mock_response(mock_urlopen,
                                {'data': {'playerMuted': True}})
        response = await client.call_tool("player_set_muted",
                                          {"id": 3,
                                           "muted": True})
        mock_urlopen.assert_called_once()
        assert 'Muted' in str(response)


@pytest.mark.asyncio
@patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
async def test_player_set_speedometer_visibility(mock_urlopen):
    async with Client(mcp) as client:
        configure_mock_response(mock_urlopen,
                                {'data': {'playerSpeedometerVisible': True}})
        response = await client.call_tool("player_set_"
                                          "speedometer_visibility",
                                          {"id": 3,
                                           "visible": True})
        mock_urlopen.assert_called_once()
        assert 'Visible' in str(response)


@pytest.mark.asyncio
@patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
async def test_player_sync(mock_urlopen):
    async with Client(mcp) as client:
        configure_mock_response(mock_urlopen,
                                {'data': {'playerSynced': True}})
        response = await client.call_tool("player_sync",
                                          {"id": 3})
        mock_urlopen.assert_called_once()
        assert 'Synced' in str(response)


@pytest.mark.asyncio
@patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
async def test_player_get_content_id(mock_urlopen):
    async with Client(mcp) as client:
        configure_mock_response(mock_urlopen,
                                mock_players)
        response = await client.call_tool("player_get_content_id")
        mock_urlopen.assert_called_once()
        assert '1000001067' in str(response)


@pytest.mark.asyncio
@patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
async def test_player_get_content_id_no_players(mock_urlopen):
    async with Client(mcp) as client:
        configure_mock_response(mock_urlopen,
                                {"data": {"players": []}})
        response = await client.call_tool("player_get_content_id")
        mock_urlopen.assert_called_once()
        assert 'No players' in str(response)
