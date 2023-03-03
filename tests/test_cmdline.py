import json

from unittest import TestCase
from unittest.mock import patch

from click.testing import CliRunner
from mvf1.cmdline import cli

from urllib.error import URLError
from mvf1 import MultiViewerForF1Error


f = open('tests/players.json')
mock_players = json.load(f)
f.close()


def configure_mock_response(mock_urlopen, payload):
    if isinstance(payload, Exception) or isinstance(payload, list):
        mock_urlopen.side_effect = payload
    else:
        mock_urlopen.return_value = payload


class TestMultiViewerForF1CommandLineInterfacePlayers(TestCase):
    def setUp(self):
        self.runner = CliRunner()

    @patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
    def test_players_ls(self, mock_urlopen):
        configure_mock_response(mock_urlopen,
                                mock_players)

        response = self.runner.invoke(cli, ["players", "ls"])

        self.assertEqual(response.exit_code, 0)
        self.assertIn("INTERNATIONAL", response.output)

    @patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
    def test_players_ls_verbose(self, mock_urlopen):
        configure_mock_response(mock_urlopen,
                                mock_players)

        response = self.runner.invoke(cli, ["players",
                                            "ls",
                                            "--verbose"])

        self.assertEqual(response.exit_code, 0)
        self.assertIn("streamData", response.output)

    @patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
    def test_players_ls_no_active_players(self, mock_urlopen):
        configure_mock_response(mock_urlopen,
                                {"data": {"players": []}})

        response = self.runner.invoke(cli, ["players", "ls"])

        self.assertEqual(response.exit_code, 2)
        self.assertIn("No active players", response.output)

    @patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
    def test_players_mute(self, mock_urlopen):
        configure_mock_response(mock_urlopen,
                                mock_players)

        response = self.runner.invoke(cli, ["players", "mute"])

        self.assertEqual(response.exit_code, 0)
        self.assertIn("INTERNATIONAL", response.output)

    @patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
    def test_players_close(self, mock_urlopen):
        configure_mock_response(mock_urlopen,
                                mock_players)

        response = self.runner.invoke(cli, ["players", "close"])

        self.assertEqual(response.exit_code, 0)
        self.assertIn("INTERNATIONAL", response.output)

    @patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
    def test_players_pause(self, mock_urlopen):
        configure_mock_response(mock_urlopen,
                                mock_players)

        response = self.runner.invoke(cli, ["players", "pause"])

        self.assertEqual(response.exit_code, 0)
        self.assertIn("INTERNATIONAL", response.output)

    @patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
    def test_players_pause_exceptions(self, mock_urlopen):
        side_effects = [
            mock_players,
            URLError("Whoopsie doodle!"),
            mock_players,
            MultiViewerForF1Error("Whoopsie doodle!"),
            mock_players,
            Exception("Whoopsie doodle!")
        ]

        configure_mock_response(mock_urlopen,
                                side_effects)

        for i in range(3):
            response = self.runner.invoke(cli, ["players", "pause"])

            self.assertEqual(response.exit_code, 2)
            self.assertIn("error", response.output.lower())

    @patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
    def test_players_mute_exceptions(self, mock_urlopen):
        side_effects = [
            mock_players,
            URLError("Whoopsie doodle!"),
            mock_players,
            MultiViewerForF1Error("Whoopsie doodle!"),
            mock_players,
            Exception("Whoopsie doodle!")
        ]

        configure_mock_response(mock_urlopen,
                                side_effects)

        for i in range(3):
            response = self.runner.invoke(cli, ["players", "mute"])

            self.assertEqual(response.exit_code, 2)
            self.assertIn("error", response.output.lower())

    @patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
    def test_players_close_exceptions(self, mock_urlopen):
        side_effects = [
            mock_players,
            URLError("Whoopsie doodle!"),
            mock_players,
            MultiViewerForF1Error("Whoopsie doodle!"),
            mock_players,
            Exception("Whoopsie doodle!")
        ]

        configure_mock_response(mock_urlopen,
                                side_effects)

        for i in range(3):
            response = self.runner.invoke(cli, ["players", "close"])

            self.assertEqual(response.exit_code, 2)
            self.assertIn("error", response.output.lower())

    @patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
    def test_players_sync(self, mock_urlopen):
        configure_mock_response(mock_urlopen,
                                mock_players)

        response = self.runner.invoke(cli, ["players", "sync"])

        self.assertEqual(response.exit_code, 0)
        self.assertIn("broadcast commentary", response.output)

    @patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
    def test_players_exceptions_gql_error(self, mock_urlopen):
        configure_mock_response(mock_urlopen,
                                MultiViewerForF1Error("Whoopsie doodle!"))

        commands = [
            ["players", "ls"],
            ["players", "mute"],
            ["players", "close"],
            ["players", "pause"],
            ["players", "sync"]
        ]

        for command in commands:
            response = self.runner.invoke(cli, command)

            self.assertEqual(response.exit_code, 2)
            self.assertIn("error", response.output)

    @patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
    def test_players_exceptions_not_running(self, mock_urlopen):
        configure_mock_response(mock_urlopen,
                                URLError("Whoopsie doodle!"))

        commands = [
            ["players", "ls"],
            ["players", "mute"],
            ["players", "close"],
            ["players", "pause"],
            ["players", "sync"]
        ]

        for command in commands:
            response = self.runner.invoke(cli, command)

            self.assertEqual(response.exit_code, 2)
            self.assertIn("not found", response.output)

    @patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
    def test_players_exceptions_generic_error(self, mock_urlopen):
        configure_mock_response(mock_urlopen,
                                Exception("Whoopsie doodle!"))

        commands = [
            ["players", "ls"],
            ["players", "mute"],
            ["players", "close"],
            ["players", "pause"],
            ["players", "sync"]
        ]

        for command in commands:
            response = self.runner.invoke(cli, command)

            self.assertEqual(response.exit_code, 2)
            self.assertIn("Error", response.output)


class TestMultiViewerForF1CommandLineInterfacePlayer(TestCase):
    def setUp(self):
        self.runner = CliRunner()

    @patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
    def test_player_query(self, mock_urlopen):
        configure_mock_response(mock_urlopen,
                                {'data': {'player':
                                          mock_players['data']['players'][0]}})

        response = self.runner.invoke(cli, ["player", "--id", "3", "query"])

        self.assertEqual(response.exit_code, 0)
        self.assertIn("INTERNATIONAL", response.output)

    @patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
    def test_player_query_verbose(self, mock_urlopen):
        configure_mock_response(mock_urlopen,
                                {'data': {'player':
                                          mock_players['data']['players'][0]}})

        response = self.runner.invoke(cli, ["player", "--id", "3", "query",
                                            "--verbose"])

        self.assertEqual(response.exit_code, 0)
        self.assertIn("INTERNATIONAL", response.output)
        self.assertIn("streamData", response.output)

    @patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
    def test_player_query_by_title(self, mock_urlopen):
        configure_mock_response(mock_urlopen,
                                mock_players)

        response = self.runner.invoke(cli, ["player", "--title", "INTERNATIONAL", "query"])

        self.assertEqual(response.exit_code, 0)
        self.assertIn("INTERNATIONAL", response.output)

        response = self.runner.invoke(cli, ["player", "--title", "YOOOO", "query"])

        self.assertEqual(response.exit_code, 2)
        self.assertIn("No player", response.output)

    @patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
    def test_player_query_exceptions(self, mock_urlopen):
        side_effects = [
            URLError("Whoopsie doodle!"),
            MultiViewerForF1Error("Whoopsie doodle!"),
            Exception("Whoopsie doodle!"),
            URLError("Whoopsie doodle!"),
            MultiViewerForF1Error("Whoopsie doodle!"),
            Exception("Whoopsie doodle!")
        ]

        configure_mock_response(mock_urlopen,
                                side_effects)

        commands = [
            ["player", "--id", "3", "query"],
            ["player", "--id", "3", "query"],
            ["player", "--id", "3", "query"],
            ["player", "--title", "INTERNATIONAL", "query"],
            ["player", "--title", "INTERNATIONAL", "query"],
            ["player", "--title", "INTERNATIONAL", "query"],
        ]

        for command in commands:
            response = self.runner.invoke(cli, command)

            self.assertEqual(response.exit_code, 2)
            self.assertIn("Error", response.output)

    @patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
    def test_player_close(self, mock_urlopen):
        configure_mock_response(mock_urlopen,
                                {'data': {'player':
                                          mock_players['data']['players'][0]}})

        response = self.runner.invoke(cli, ["player", "--id", "3", "close"])

        self.assertEqual(response.exit_code, 0)
        self.assertIn("INTERNATIONAL", response.output)

    @patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
    def test_player_mute(self, mock_urlopen):
        configure_mock_response(mock_urlopen,
                                {'data': {'player':
                                          mock_players['data']['players'][0]}})

        response = self.runner.invoke(cli, ["player", "--id", "3", "mute"])

        self.assertEqual(response.exit_code, 0)
        self.assertIn("INTERNATIONAL", response.output)

    @patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
    def test_player_always_on_top(self, mock_urlopen):
        configure_mock_response(mock_urlopen,
                                {'data': {'player':
                                          mock_players['data']['players'][0]}})

        response = self.runner.invoke(cli, ["player",
                                            "--id",
                                            "3",
                                            "set-always-on-top"])

        self.assertEqual(response.exit_code, 0)
        self.assertIn("INTERNATIONAL", response.output)

    @patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
    def test_player_pause(self, mock_urlopen):
        configure_mock_response(mock_urlopen,
                                {'data': {'player':
                                          mock_players['data']['players'][0]}})

        response = self.runner.invoke(cli, ["player", "--id", "3", "pause"])

        self.assertEqual(response.exit_code, 0)
        self.assertIn("INTERNATIONAL", response.output)

    @patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
    def test_player_sync(self, mock_urlopen):
        configure_mock_response(mock_urlopen,
                                {'data': {'player':
                                          mock_players['data']['players'][0]}})

        response = self.runner.invoke(cli, ["player", "--id", "3", "sync"])

        self.assertEqual(response.exit_code, 0)
        self.assertIn("INTERNATIONAL", response.output)

    @patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
    def test_player_seek(self, mock_urlopen):
        configure_mock_response(mock_urlopen,
                                {'data': {'player':
                                          mock_players['data']['players'][0]}})

        response = self.runner.invoke(cli, ["player",
                                            "--id", "3",
                                            "seek", "--relative", "200"])

        self.assertEqual(response.exit_code, 0)
        self.assertIn("INTERNATIONAL", response.output)

    @patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
    def test_player_seek_no_options(self, mock_urlopen):
        configure_mock_response(mock_urlopen,
                                {'data': {'player':
                                          mock_players['data']['players'][0]}})

        response = self.runner.invoke(cli, ["player",
                                            "--id", "3",
                                            "seek"])

        self.assertEqual(response.exit_code, 2)
        self.assertIn("To seek", response.output)

    @patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
    def test_player_set_bounds(self, mock_urlopen):
        configure_mock_response(mock_urlopen,
                                {'data': {'player':
                                          mock_players['data']['players'][0]}})

        response = self.runner.invoke(cli, ["player",
                                            "--id", "3",
                                            "set-bounds",
                                            "--x", "0",
                                            "--y", "0",
                                            "--width", "640",
                                            "--height", "480"])

        self.assertEqual(response.exit_code, 0)
        self.assertIn("INTERNATIONAL", response.output)

    @patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
    def test_player_set_volume(self, mock_urlopen):
        configure_mock_response(mock_urlopen,
                                {'data': {'player':
                                          mock_players['data']['players'][0]}})

        response = self.runner.invoke(cli, ["player", "--id", "3",
                                            "set-volume", "--volume", "28"])

        self.assertEqual(response.exit_code, 0)
        self.assertIn("INTERNATIONAL", response.output)

    @patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
    def test_player_set_fullscreen(self, mock_urlopen):
        configure_mock_response(mock_urlopen,
                                {'data': {'player':
                                          mock_players['data']['players'][0]}})

        response = self.runner.invoke(cli, ["player", "--id", "3",
                                            "set-fullscreen"])

        self.assertEqual(response.exit_code, 0)
        self.assertIn("INTERNATIONAL", response.output)

    @patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
    def test_player_set_speedometer_visibility(self, mock_urlopen):
        configure_mock_response(mock_urlopen,
                                {'data': {'player':
                                          mock_players['data']['players'][0]}})

        response = self.runner.invoke(cli, ["player", "--id", "3",
                                            "set-speedometer-visibility"])

        self.assertEqual(response.exit_code, 0)
        self.assertIn("INTERNATIONAL", response.output)

    @patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
    def test_player_switch_stream(self, mock_urlopen):
        side_effects = [
            {"data": {"player": mock_players['data']['players'][0]}},
            {'data': {'playerDelete': True}},
            {'data': {'playerCreate': 5}},
            {"data": {"player": mock_players['data']['players'][0]}}
        ]
        configure_mock_response(mock_urlopen,
                                side_effects)

        response = self.runner.invoke(cli, ["player", "--id", "4",
                                            "switch-stream", "--title",
                                            "INTERNATIONAL"])

        self.assertEqual(response.exit_code, 0)
        self.assertIn("INTERNATIONAL", response.output)

    @patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
    def test_player_exceptions_gql_error(self, mock_urlopen):
        side_effects = [
            {"data": {"player": mock_players['data']['players'][0]}},
            MultiViewerForF1Error("Whoopsie doodle!"),
            {"data": {"player": mock_players['data']['players'][0]}},
            MultiViewerForF1Error("Whoopsie doodle!"),
            {"data": {"player": mock_players['data']['players'][0]}},
            MultiViewerForF1Error("Whoopsie doodle!"),
            {"data": {"player": mock_players['data']['players'][0]}},
            MultiViewerForF1Error("Whoopsie doodle!"),
            {"data": {"player": mock_players['data']['players'][0]}},
            MultiViewerForF1Error("Whoopsie doodle!"),
            {"data": {"player": mock_players['data']['players'][0]}},
            MultiViewerForF1Error("Whoopsie doodle!"),
            {"data": {"player": mock_players['data']['players'][0]}},
            MultiViewerForF1Error("Whoopsie doodle!"),
            {"data": {"player": mock_players['data']['players'][0]}},
            MultiViewerForF1Error("Whoopsie doodle!"),
            {"data": {"player": mock_players['data']['players'][0]}},
            MultiViewerForF1Error("Whoopsie doodle!"),
            {"data": {"player": mock_players['data']['players'][0]}},
            MultiViewerForF1Error("Whoopsie doodle!"),
            {"data": {"player": mock_players['data']['players'][0]}},
            MultiViewerForF1Error("Whoopsie doodle!"),
            {"data": {"player": mock_players['data']['players'][0]}},
            MultiViewerForF1Error("Whoopsie doodle!")
        ]
        configure_mock_response(mock_urlopen,
                                side_effects)

        commands = [
            ["player", "--id", "3", "mute"],
            ["player", "--id", "3", "close"],
            ["player", "--id", "3", "pause"],
            ["player", "--id", "3", "sync"],
            ["player", "--id", "3", "mute"],
            ["player", "--id", "3", "set-always-on-top"],
            ["player", "--id", "3", "set-fullscreen"],
            ["player", "--id", "3", "set-speedometer-visibility"],
            ["player", "--id", "3", "seek", "--relative", "300"],
            ["player", "--id", "3", "set-volume", "--volume", "28"],
            ["player", "--id", "3", "set-bounds", "--x", "0", "--y", "0"],
            ["player", "--id", "3", "switch-stream", "--title", "INTERNATIONAL"]
        ]

        for command in commands:
            response = self.runner.invoke(cli, command)

            self.assertEqual(response.exit_code, 2)
            self.assertIn("error", response.output)

    @patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
    def test_player_exceptions_not_running(self, mock_urlopen):
        side_effects = [
            {"data": {"player": mock_players['data']['players'][0]}},
            URLError("Whoopsie doodle!"),
            {"data": {"player": mock_players['data']['players'][0]}},
            URLError("Whoopsie doodle!"),
            {"data": {"player": mock_players['data']['players'][0]}},
            URLError("Whoopsie doodle!"),
            {"data": {"player": mock_players['data']['players'][0]}},
            URLError("Whoopsie doodle!"),
            {"data": {"player": mock_players['data']['players'][0]}},
            URLError("Whoopsie doodle!"),
            {"data": {"player": mock_players['data']['players'][0]}},
            URLError("Whoopsie doodle!"),
            {"data": {"player": mock_players['data']['players'][0]}},
            URLError("Whoopsie doodle!"),
            {"data": {"player": mock_players['data']['players'][0]}},
            URLError("Whoopsie doodle!"),
            {"data": {"player": mock_players['data']['players'][0]}},
            URLError("Whoopsie doodle!"),
            {"data": {"player": mock_players['data']['players'][0]}},
            URLError("Whoopsie doodle!"),
            {"data": {"player": mock_players['data']['players'][0]}},
            URLError("Whoopsie doodle!"),
            {"data": {"player": mock_players['data']['players'][0]}},
            URLError("Whoopsie doodle!")
        ]
        configure_mock_response(mock_urlopen,
                                side_effects)

        commands = [
            ["player", "--id", "3", "mute"],
            ["player", "--id", "3", "close"],
            ["player", "--id", "3", "pause"],
            ["player", "--id", "3", "sync"],
            ["player", "--id", "3", "mute"],
            ["player", "--id", "3", "set-always-on-top"],
            ["player", "--id", "3", "set-fullscreen"],
            ["player", "--id", "3", "seek", "--relative", "300"],
            ["player", "--id", "3", "set-speedometer-visibility"],
            ["player", "--id", "3", "set-volume", "--volume", "28"],
            ["player", "--id", "3", "set-bounds", "--x", "0", "--y", "0"],
            ["player", "--id", "3", "switch-stream", "--title", "INTERNATIONAL"]
        ]

        for command in commands:
            response = self.runner.invoke(cli, command)

            self.assertEqual(response.exit_code, 2)
            self.assertIn("error", response.output.lower())

    @patch('sgqlc.endpoint.http.HTTPEndpoint.__call__')
    def test_player_exceptions_generic_error(self, mock_urlopen):
        side_effects = [
            {"data": {"player": mock_players['data']['players'][0]}},
            Exception("Whoopsie doodle!"),
            {"data": {"player": mock_players['data']['players'][0]}},
            Exception("Whoopsie doodle!"),
            {"data": {"player": mock_players['data']['players'][0]}},
            Exception("Whoopsie doodle!"),
            {"data": {"player": mock_players['data']['players'][0]}},
            Exception("Whoopsie doodle!"),
            {"data": {"player": mock_players['data']['players'][0]}},
            Exception("Whoopsie doodle!"),
            {"data": {"player": mock_players['data']['players'][0]}},
            Exception("Whoopsie doodle!"),
            {"data": {"player": mock_players['data']['players'][0]}},
            Exception("Whoopsie doodle!"),
            {"data": {"player": mock_players['data']['players'][0]}},
            Exception("Whoopsie doodle!"),
            {"data": {"player": mock_players['data']['players'][0]}},
            Exception("Whoopsie doodle!"),
            {"data": {"player": mock_players['data']['players'][0]}},
            Exception("Whoopsie doodle!"),
            {"data": {"player": mock_players['data']['players'][0]}},
            Exception("Whoopsie doodle!"),
            {"data": {"player": mock_players['data']['players'][0]}},
            Exception("Whoopsie doodle!")
        ]
        configure_mock_response(mock_urlopen,
                                side_effects)

        commands = [
            ["player", "--id", "3", "mute"],
            ["player", "--id", "3", "close"],
            ["player", "--id", "3", "pause"],
            ["player", "--id", "3", "sync"],
            ["player", "--id", "3", "mute"],
            ["player", "--id", "3", "set-always-on-top"],
            ["player", "--id", "3", "set-fullscreen"],
            ["player", "--id", "3", "set-speedometer-visibility"],
            ["player", "--id", "3", "seek", "--relative", "300"],
            ["player", "--id", "3", "set-volume", "--volume", "28"],
            ["player", "--id", "3", "set-bounds", "--x", "0", "--y", "0"],
            ["player", "--id", "3", "switch-stream", "--title", "INTERNATIONAL"]
        ]

        for command in commands:
            response = self.runner.invoke(cli, command)

            self.assertEqual(response.exit_code, 2)
            self.assertIn("error", response.output.lower())
