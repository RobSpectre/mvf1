import logging
import time
from datetime import datetime
from typing import Optional

import requests
from sgqlc.operation import Operation
from sgqlc.endpoint.http import HTTPEndpoint

from .mvf1_schema import mvf1_schema as schema
from .mvf1_schema import PlayerCreateInput
from .mvf1_schema import RectangleInput


class MultiViewerForF1(object):
    """
    A class to control video players for MultiViewerForF1, the best way to
    watch Formula 1.

    To download the app, visit their website at https://multiviewer.app/.

    Parameters
    ----------
    uri: str, optional
    Uri to control the MultiViewerForF1 install.
    Defaults to http://localhost:101010/api/graphql

    Attributes
    ----------
    endpoint: HTTPEndpoint
        GraphQL API Endpoint of MultiViewerForF1.

    """

    def __init__(self, uri="http://localhost:10101/api/graphql"):
        self.endpoint = HTTPEndpoint(uri)

    def perform_operation(self,
                          operation: Operation) -> dict:
        """
        Performs the GraphQL operation.

        Parameters
        ----------
        operation: Operation
            GraphQL Operation.

        Returns
        -------
        dict
            MultiViewerForF1 API Response.

        """
        response = self.endpoint(operation)

        if "errors" in response:
            error = response["errors"][0]
            raise MultiViewerForF1Error(f"{error['message']}")
        else:
            return response

    @property
    def live_timing_clock(self) -> dict:
        """
        Returns the time for an event when it is live.

        Returns
        -------
        dict
            Current time.

        """
        operation = Operation(schema.Query)
        operation.f1_live_timing_clock()

        return self.perform_operation(operation)

    @property
    def live_timing_state(self) -> dict:
        """
        Returns state of live timing at current time.

        Returns
        -------
        dict
            Current state.

        """
        operation = Operation(schema.Query)
        operation.f1_live_timing_state()

        return self.perform_operation(operation)

    @property
    def f1_live_timing_clock(self) -> dict:
        """
        Returns the time for an event when it is live.

        Returns
        -------
        dict
            Current time.

        """
        operation = Operation(schema.Query)
        operation.f1_live_timing_clock()

        return self.perform_operation(operation)

    @property
    def f1_live_timing_state(self) -> dict:
        """
        Returns state of live timing at current time.

        Returns
        -------
        dict
            Current state.

        """
        operation = Operation(schema.Query)
        operation.f1_live_timing_state()

        return self.perform_operation(operation)

    @property
    def fiawec_live_timing_state(self) -> dict:
        """
        Returns state of live timing at current time.

        Returns
        -------
        dict
            Current state.

        """
        operation = Operation(schema.Query)
        operation.fiawec_live_timing_state()

        return self.perform_operation(operation)

    @property
    def players(self) -> list:
        """
        Returns a list of active MultiViewerForF1 players.

        Returns
        -------
        list
            List of Player objects.

        """
        operation = Operation(schema.Query)
        operation.players()

        players_data = self.perform_operation(operation)

        players = []

        for player_data in players_data["data"]["players"]:
            players.append(Player(player_data))

        return players

    @property
    def system_info(self) -> dict:
        """
        Returns the system information.

        Returns
        -------
        dict
            System information.

        """
        operation = Operation(schema.Query)
        operation.system_info()

        return self.perform_operation(operation)

    @property
    def version(self) -> dict:
        """
        Returns the MultiViewerForF1 version.

        Returns
        -------
        dict
            Version information.

        """
        operation = Operation(schema.Query)
        operation.version()

        return self.perform_operation(operation)

    def player(self, id: int) -> "Player":
        """
        Returns the player with specific id.

        Parameters
        ----------
        id: int
            Id of player.

        Returns
        -------
        dict
            Player object.

        """
        operation = Operation(schema.Query)
        operation.player(id=id)

        player_data = self.perform_operation(operation)
        return Player(player_data["data"]["player"])

    def player_create(
        self,
        content_id: int,
        driver_tla: Optional[str] = None,
        driver_number: Optional[int] = None,
        stream_title: Optional[str] = None,
        x: Optional[int] = None,
        y: Optional[int] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        fullscreen: Optional[bool] = False,
        always_on_top: Optional[bool] = False,
        maintain_aspect_ratio: Optional[bool] = True,
    ) -> dict:
        """
        Creates a new player.

        Parameters
        ----------
        content_id: int
            Content Id.

        driver_tla: str, optional
            Driver three letter acronym (e.g. 'PER' or 'HAM').

        driver_number: int, optional
            Driver Number.

        stream_title: str, optional
            Stream Title.

        x: int, optional
            X coordinate of player's top left corner.

        y: int, optional
            Y coordinate of player's top left corner.

        width: int, optional
            Width of player.

        height: int, optional
            Height of player.

        fullscreen: bool, optional
            Fullscreen status.

        always_on_top: bool, optional
            Always on top status.

        maintain_aspect_ratio: bool, optional
            Maintain aspect ratio status.

        Returns
        -------
        dict
            Dict with result of playerCreate operation. If successful, will
            include the `player_id`.

            Implementation note: we return a `player_id` instead of a `Player`
            object is that there is ~200-800 millisecond lag in between the
            invocation of `player_create` and the `player_id` being accessible
            via the MultiViewer For F1 GraphQL API.  Player creation is
            non-blocking and there is no callback when it is complete. As a
            consequence, we leave this as an implmentation decision for you.

            Most folks put a sleep in between player creation and player
            access.
        """
        operation = Operation(schema.Mutation)

        if x or y or width or height:
            bounds = RectangleInput(x=x, y=y, width=width, height=height)
        else:
            bounds = None

        player = PlayerCreateInput(
            content_id=content_id,
            driver_tla=driver_tla,
            driver_number=driver_number,
            stream_title=stream_title,
            bounds=bounds,
            fullscreen=fullscreen,
            always_on_top=always_on_top,
            maintain_aspect_ratio=maintain_aspect_ratio,
        )

        operation.player_create(input=player)

        player_data = self.perform_operation(operation)

        return player_data

    def player_delete(self, id: int) -> dict:
        """
        Deletes a player.

        Parameters
        ----------
        id: int
            Id of player.

        Returns
        -------
        dict
            Deletion response.

        """
        operation = Operation(schema.Mutation)
        operation.player_delete(id=id)

        return self.perform_operation(operation)

    def player_seek_to(
        self,
        id: int,
        absolute: Optional[float] = None,
        relative: Optional[float] = None,
    ) -> dict:
        """
        Seeks to a specific position.

        Parameters
        ----------
        id: int
            Id of player.

        absolute: float, optional
            Absolute position.

        relative: float, optional
            Relative position.

        Returns
        -------
        dict
            Seek response.

        """
        operation = Operation(schema.Mutation)
        operation.player_seek_to(id=id, absolute=absolute, relative=relative)

        return self.perform_operation(operation)

    def player_set_bounds(
        self,
        id: int,
        x: Optional[int] = None,
        y: Optional[int] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
    ) -> dict:
        """
        Set the bounds of a player.

        Parameters
        ----------
        id: int
            Id of player.

        x: int, optional
            X coordinate of player's top left corner.

        y: int, optional
            Y coordinate of player's top left corner.

        width: int, optional
            Width of player.

        height: int, optional
            Height of player.

        Returns
        -------
        dict
            True if operation is successful.

        """
        operation = Operation(schema.Mutation)

        bounds = RectangleInput(x=x, y=y, width=width, height=height)

        operation.player_set_bounds(id=id, bounds=bounds)

        return self.perform_operation(operation)

    def player_set_volume(self, id: int, volume: int) -> dict:
        """
        Set the volume of a player.

        Parameters
        ----------
        id: int
            Id of player.

        volume: int
            Volume of player.

        Returns
        -------
        dict
            True if operation is successful.

        """
        operation = Operation(schema.Mutation)
        operation.player_set_volume(id=id, volume=volume)

        return self.perform_operation(operation)

    def player_set_paused(self, id: int, paused: Optional[bool] = None) -> dict:
        """
        Pauses/unpauses player or specifies pause state for player.

        Parameters
        ----------
        id: int
            Id of player.

        paused: bool, optional
            Desired pause state for player.

        Returns
        -------
        dict
            True if operation is successful.

        """
        operation = Operation(schema.Mutation)
        operation.player_set_paused(id=id, paused=paused)

        return self.perform_operation(operation)

    def player_set_fullscreen(self, id: int, fullscreen: Optional[bool] = None) -> dict:
        """
        Toggles fullscreen for a player or specifies fullscreen state for
        player.

        Parameters
        ----------
        id: int
            Id of player.

        fullscreen: bool, optional
            Desired fullscreen state of player.

        Returns
        -------
        dict
            True if operation is successful.

        """
        operation = Operation(schema.Mutation)
        operation.player_set_fullscreen(id=id, fullscreen=fullscreen)

        return self.perform_operation(operation)

    def player_set_muted(self, id: int, muted: Optional[bool] = None) -> dict:
        """
        Mutes/unmutes player or specifies muted state for player.

        Parameters
        ----------
        id: int
            Id of player.

        muted: bool, optional
            Desired muted state of player.

        Returns
        -------
        dict
            True if operation is successful.

        """
        operation = Operation(schema.Mutation)
        operation.player_set_muted(id=id, muted=muted)

        return self.perform_operation(operation)

    def player_set_speedometer_visibility(
        self, id: int, visible: Optional[bool] = None
    ) -> dict:
        """
        Makes speedometer overlay on player visible/invisible or specifies
        visibility.

        Parameters
        ----------
        id: int 
            Id of player.

        visible: bool, optional
            Visibility state of speedometer of player.

        Returns
        -------
        dict
            True if operation is successful.

        """
        operation = Operation(schema.Mutation)
        operation.player_set_speedometer_visibility(id=id, visible=visible)

        return self.perform_operation(operation)

    def player_set_driver_header_mode(self,
                                      id: int,
                                      mode: Optional[str] = None) -> dict:

        """
        Sets the overlay display for a driver stream.

        Parameters
        ----------
        id: int
            Id of player.

        mode: str, optional
            Desired overlay of the player - can be DRIVER_HEADER, NONE or
            OBC_LIVE_TIMING

        Returns
        -------
        dict
            True if operation is successful.

        """
        operation = Operation(schema.Mutation)

        operation.player_set_driver_header_mode(id=id, mode=mode)

        try:
            return self.perform_operation(operation)
        except ValueError as e:
            raise MultiViewerForF1Error(f"{e} - can be DRIVER_HEADER, NONE"
                                         " or OBC_LIVE_TIMING.")

    def player_set_always_on_top(
        self, id: int, always_on_top: Optional[bool] = None
    ) -> dict:
        """
        Sets player on/off always on top.

        Parameters
        ----------
        id: int 
            Id of player.

        always_on_top: bool, optional
            Is the player always on top?

        Returns
        -------
        dict
            True if operation is successful.

        """
        operation = Operation(schema.Mutation)
        operation.player_set_always_on_top(id=id, always_on_top=always_on_top) 

        return self.perform_operation(operation)

    def player_sync(self, id: int) -> dict:
        """
        Synchronizes all players to the timestamp of specified player.

        Parameters
        ----------
        id: int
            Id of player.

        Returns
        -------
        dict
            True if operation is successful.

        """
        operation = Operation(schema.Mutation)
        operation.player_sync(id=id)

        return self.perform_operation(operation)

    def player_sync_to_commentary(self) -> dict:
        """
        Synchronizes all players to the player with a broadcast commentary stream.

        Returns
        -------
        dict
            True if operation is successful.

        """
        for player in self.players:
            if (
                player.stream_data["title"] == "INTERNATIONAL"
                or player.stream_data["title"] == "F1 LIVE"
            ):
                return player.sync()

        return {"data": "No player has commentary."}

    def player_sync_to_live_timing(self) -> dict:
        """Synchronize open players to the current live-timing position.

        The session is resolved from the first open player with meeting and
        session metadata. The sessions API's ``session_start`` offset, the
        live-timing clock, and the first ``SessionStatus=Started`` event are
        used to derive the video position, matching MultiViewer's replay
        live-timing sync calculation. No video player is used as the
        synchronization source.

        Returns
        -------
        dict
            A summary of the players synchronized to live timing.

        """
        players = self.players
        session_player = next(
            (
                player
                for player in players
                if player.stream_data.get("meetingKey")
                and player.stream_data.get("sessionKey")
            ),
            None,
        )
        if session_player is None:
            return {
                "data": {
                    "synced_players": [],
                    "message": "No players with session metadata are active.",
                }
            }

        meeting_id = session_player.stream_data["meetingKey"]
        session_id = session_player.stream_data["sessionKey"]
        url = (
            "https://api.multiviewer.dev/api/v1/meetings/"
            f"{meeting_id}/sessions/{session_id}"
        )
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        timing_data = response.json()
        try:
            session_start = float(timing_data["session_start"])
            clock = self.f1_live_timing_clock["data"]["f1LiveTimingClock"]
            timing_position = float(clock["trackTime"])
            if not clock["paused"]:
                timing_position += (
                    time.time() * 1000 - float(clock["systemTime"])
                )

            timing_state = self.f1_live_timing_state["data"][
                "f1LiveTimingState"
            ]
            status_series = timing_state["SessionData"]["StatusSeries"]
            session_started = next(
                item
                for item in status_series
                if item.get("SessionStatus") == "Started" and item.get("Utc")
            )
            session_started_at = datetime.fromisoformat(
                session_started["Utc"].replace("Z", "+00:00")
            ).timestamp() * 1000
            position = session_start + (
                timing_position - session_started_at
            ) / 1000
        except (KeyError, StopIteration, TypeError, ValueError):
            return {
                "data": {
                    "meeting_id": str(meeting_id),
                    "session_id": str(session_id),
                    "synced_players": [],
                    "message": "Live timing position is unavailable.",
                }
            }

        synced_players = []
        skipped_live_players = []
        for player in players:
            if (
                str(player.stream_data.get("meetingKey")) != str(meeting_id)
                or str(player.stream_data.get("sessionKey")) != str(session_id)
            ):
                continue

            if player.state and player.state.get("live"):
                skipped_live_players.append(
                    {
                        "id": player.id,
                        "title": player.title,
                        "reason": (
                            "MultiViewer does not expose live-stream seeking "
                            "via GraphQL."
                        ),
                    }
                )
                continue

            result = self.player_seek_to(player.id, absolute=position)
            synced_players.append(
                {
                    "id": player.id,
                    "title": player.title,
                    "position": position,
                    "result": result,
                }
            )

        return {
            "data": {
                "meeting_id": str(meeting_id),
                "session_id": str(session_id),
                "position": position,
                "session_started_at": session_started["Utc"],
                "synced_players": synced_players,
                "skipped_live_players": skipped_live_players,
            }
        }

    def content_ids(self, meeting_key: str) -> dict:
        """
        Retrieves contentIds for all sessions in a meeting from the
        MultiViewer meetings API.

        To create a video player with `player_create`, get the meeting key
        from `f1_live_timing_state` (SessionInfo.Meeting.Key), pass it to
        this method to get the session contentIds, then pick the contentId
        for the session you want to watch.

        Parameters
        ----------
        meeting_key: str
            Meeting key from f1_live_timing_state.

        Returns
        -------
        dict
            Dictionary mapping session titles to their F1 TV contentIds.

        """
        url = f"https://api.multiviewer.app/api/v1/meetings/{meeting_key}"
        response = requests.get(url)
        response.raise_for_status()

        content_ids = {}
        for session in response.json().get("sessions", []):
            title = session.get("title")
            content_id = session.get("f1tv_content_id")
            if title and content_id:
                content_ids[title] = content_id
        return content_ids


class Player(object):
    """
    Encapsulate the behaviour of Player.

    Attributes
    ----------
    id: int
        Player Id.
    state: str
        Player state.
    driver_data: dict
        Player driver_data.
    stream_data: dict
        Player stream_data.
    content_id: int
        Player F1TV Content ID.
    channel_id: int
        Player F1TV Channel ID.
    title: str
        Title of stream playing in player.
    bounds: dict
        Player bounds.
    x: float
        X coordinate of player's top left corner.
    y: float
        Y coordinate of player's top left corner.
    width: float
        Width of player.
    height: float
        Height of player.
    fullscreen: bool
        Is player fullscreen?
    always_on_top: bool
        Is player always on top?
    maintain_aspect_ratio: bool
        Does player maintain aspect ratio?
    remote: MultiViewerForF1
        Interface to control MultiViewerForF1.
    """

    def __init__(self, player_dict: dict):
        self.id = player_dict["id"]
        self.state = player_dict["state"]
        self.driver_data = player_dict["driverData"]
        self.stream_data = player_dict["streamData"]
        self.content_id = self.stream_data["contentId"]
        self.channel_id = self.stream_data["channelId"]
        self.title = self.stream_data["title"]
        self.bounds = player_dict["bounds"]
        self.x = self.bounds["x"]
        self.y = self.bounds["y"]
        self.width = self.bounds["width"]
        self.height = self.bounds["height"]
        self.fullscreen = player_dict["fullscreen"]
        self.always_on_top = player_dict["alwaysOnTop"]
        self.maintain_aspect_ratio = player_dict["maintainAspectRatio"]
        self.remote = MultiViewerForF1()

    def __repr__(self) -> str:
        """
        String representing the player object

        Returns
        -------
        str
            String representing the player object.

        """
        return f"{self.id}: {self.stream_data['title']}"

    def delete(self) -> dict:
        """
        Delete this player.

        Returns
        -------
        dict
            Response of deletion operation.
        """
        return self.remote.player_delete(self.id)

    def seek(
        self, absolute: Optional[int] = None, relative: Optional[int] = None
    ) -> dict:
        """
        Seeks this player's timestamp to an absolute or relative position.

        Parameters
        ----------
        absolute: float, optional
            Absolute value.
        relative: float, optional
            Relative value.

        Returns
        -------
        dict
            Server response of this player's seek operation.

        """
        return self.remote.player_seek_to(self.id, absolute=absolute, relative=relative)

    def set_bounds(
        self,
        x: Optional[int] = None,
        y: Optional[int] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
    ) -> dict:
        """
        Set bounds of this player.

        Parameters
        ----------
        x: int, optional
            X coordinate of this player's top left corner.
        y: int, optional
            Y coordinate of this player's top left corner.
        width: int, optional
            Width of player.
        height: int, optional
            Height of player.

        Returns
        -------
        dict
            Server response of setting this player's bounds.


        """
        return self.remote.player_set_bounds(
            self.id, x=x, y=y, width=width, height=height
        )

    def set_volume(self, volume: int) -> dict:
        """
        Set volume of this player.

        Parameters
        ----------
        volume: int, optional
            Desired volume of this player.

        Returns
        -------
        dict
            Server response of setting this player's volume.


        """
        return self.remote.player_set_volume(self.id, volume=volume)

    def pause(self, paused: Optional[bool] = None) -> dict:
        """
        Pauses/unpauses player or specifies pause state for player.

        Parameters
        ----------
        paused: bool, optional
            Desired pause state of this player.

        Returns
        -------
        dict
            Server response of this player's pause state.


        """
        return self.remote.player_set_paused(self.id, paused=paused)

    def set_fullscreen(self, fullscreen: Optional[bool] = None) -> dict:
        """
        Toggles fullscreen for a player or specifies fullscreen state for
          player.

        Parameters
        ----------
        fullscreen: bool, optional
            Desired fullscreen state of this player.

        Returns
        -------
        dict
            Server response of this player's fullscreen state.


        """
        return self.remote.player_set_fullscreen(self.id, fullscreen=fullscreen)

    def mute(self, muted: Optional[bool] = None) -> dict:
        """
        Mutes/unmutes player or specifies muted state for player.

        Parameters
        ----------
        muted: bool, optional
            Mute the player.

        Returns
        -------
        dict
            Server response of this player's muted state.


        """
        return self.remote.player_set_muted(self.id, muted=muted)

    def set_speedometer_visibility(self, visible: Optional[bool] = None) -> dict:
        """
        Makes speedometer overlay on this player visible/invisible or specifies
          visibility.

        Parameters
        ----------
        visible: bool, optional
            Visibility of speedometer overlay on this player.

        Returns
        -------
        dict
            Server response fo this player's speedometer visibility.


        """
        return self.remote.player_set_speedometer_visibility(self.id, visible=visible)

    def set_driver_header_mode(self, mode: Optional[str] = None) -> dict:
        """
        Sets the overlay display for a driver stream.

        Parameters
        ----------
        id: int
            Id of player.

        mode: str, optional
            Desired overlay of the player - can be DRIVER_HEADER, NONE or
            OBC_LIVE_TIMING

        Returns
        -------
        dict
           Server response to this player's driver header mode. 

        """

        return self.remote.player_set_driver_header_mode(self.id, mode=mode)

    def set_always_on_top(self, always_on_top: Optional[bool] = None) -> dict:
        """
        Turns player on/off always on top.

        Parameters
        ----------
        always_on_top: bool, optional
            Is the player always on top?

        Returns
        -------
        dict
            Server response fo this player's speedometer visibility.


        """
        return self.remote.player_set_always_on_top(self.id,
                                                    always_on_top=always_on_top)

    def sync(self) -> dict:
        """
        Synchronize all MultiViewerForF1 players to the timestamp of this
        player.

        Returns
        -------
        dict
            Server response of this player's sync operation.


        """
        return self.remote.player_sync(self.id)

    def switch_stream(self, title: str) -> dict:
        """
        Switch stream of this player.

        Parameters
        ----------
        title: str
            Title of stream feed (e.g. 'INTERNATIONAL' for Crofty or 'PER' for
            Checo).

        Returns
        -------
        dict 
            Dict with result of player_create operation.

            Please see the implementation note on 
            `MultiViewerForF1.player_create`.

        """
        self.delete()

        return self.remote.player_create(
            self.content_id,
            stream_title=title,
            x=self.x,
            y=self.y,
            width=self.width,
            height=self.height,
        )


class MultiViewerForF1Error(Exception):
    """
    Wrap errors from MultiViewerForF1 API.

    Attributes
    ----------
    message: str
        Error message.

    Methods
    -------
    __init__(self, message)
        Log the error.

    """

    def __init__(self, message: str):
        logging.error(f"ERROR: {message}")
