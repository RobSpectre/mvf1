from typing import Optional

from fastmcp import FastMCP

from mvf1 import MultiViewerForF1


def create_mcp_server(url: str = "http://localhost:10101/api/graphql") -> FastMCP:
    """Create and configure MCP server with custom MultiViewer URL."""
    client = MultiViewerForF1(uri=url)
    
    mcp = FastMCP(name="MultiViewer MCP Server",
                  instructions="""
                  This server provides control of MultiViewer,
                  a desktop application for watching motorsports
                  series like Formula 1, World Endurance Championship,
                  IndyCar, Formula 2, Formula 3 and Formula 1 Academy.

                  It is useful app as it provides the viewer with the
                  ability to run multiple video streams from the same
                  event successfully including the main broadcast,
                  driver onboards and data on the event.

                  Call f1_live_timing_state() for all the data about
                  the Formula 1 racing session so far.

                  Call wec_live_timing_state() for all the data about
                  the World Endurance Championship racing sesion
                  so far.

                  Call players() to get the ideas and titles for all
                  the currently running players.

                  Call the tools prefixed with players_ to create,
                  delete or manipulate existing MultiViewer video
                  players.

                  For most prompts, you will want to call the appropriate
                  live_timing tool first to get the current state
                  of the racing session (F1 or WEC only) and then call
                  players() to get the current state of all the video
                  players.

                  Note that new players take between 500-800 milliseconds
                  to full initialize - always pause before performing
                  a mutation on a freshly created player.

                  Also note that when a video is fullscreen it should be the
                  first player deployed so that subsequent players will appear
                  on top of it, creating a picture-in-picture effect.

                  Driver onboards laid on top of a fullscreen should be no
                  wider than one-fifth of the screen's width. Multiple
                  driver onboards should be tiled on the left side
                  of the screen.
                  """)

    @mcp.tool()
    def f1_live_timing_clock() -> dict:
        """
        Returns the time for a Formula 1 event when it is playing.

        Returns
        -------
        dict
            Current time.

        """
        return client.f1_live_timing_clock

    @mcp.tool()
    def f1_live_timing_state() -> dict:
        """
        Returns state of live timing for a Formula 1 event
        when it is playing. These data provide the current
        race information including racing order, lap times,
        race control messages, position on track, and
        driver telemetry.

        Returns
        -------
        dict
            Current state of Formula 1 race.

        """
        return client.f1_live_timing_state

    @mcp.tool()
    def fiawec_live_timing_state() -> dict:
        """
        Returns state of live timing for a World Endurance
        Championship event when it is playing. These data
        provide the current race information including
        racing order, lap times, race control messages,
        position on track, and driver telemetry.

        Returns
        -------
        dict
            Current state of World Endurance Championship
            race.

        """
        return client.fiawec_live_timing_state

    @mcp.tool()
    def players() -> list:
        """
        Returns a list of active MultiViewer video players
        displaying content.

        Returns
        -------
        list
            List of player information as dictionaries.

        """
        players_list = client.players
        # Convert Player objects to serializable dictionaries
        return [str(player) for player in players_list]

    @mcp.tool()
    def system_info() -> dict:
        """
        Returns the information on the system running MultiViewer.

        Returns
        -------
        dict
            System information.

        """
        return client.system_info

    @mcp.tool()
    def version() -> dict:
        """
        Returns the MultiViewer version.

        Returns
        -------
        dict
            Version information.

        """
        return client.version

    @mcp.tool()
    def player(id: int) -> str:
        """
        Returns the MultiViewer video player with specific id.

        Parameters
        ----------
        id: int
            Id of video player.

        Returns
        -------
        str
            Player information as string.

        """
        player_obj = client.player(id=id)
        return str(player_obj)

    @mcp.tool()
    def player_create(
        content_id,  # Accept both int and str
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
        Creates a new MultiViewer video player.

        Parameters
        ----------
        content_id: int or str
            The contentId for the event.

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
        return client.player_create(content_id=content_id,
                                    driver_tla=driver_tla,
                                    driver_number=driver_number,
                                    stream_title=stream_title,
                                    x=x,
                                    y=y,
                                    width=width,
                                    height=height,
                                    fullscreen=fullscreen,
                                    always_on_top=always_on_top,
                                    maintain_aspect_ratio=maintain_aspect_ratio)

    @mcp.tool()
    def player_delete(id: int) -> dict:
        """
        Deletes a MultiViewer video player.

        Parameters
        ----------
        id: int
            Id of MultiViewer video player.

        Returns
        -------
        dict
            Deletion response.

        """
        return client.player_delete(id=id)

    @mcp.tool()
    def player_seek_to(id: int,
                       absolute: Optional[int] = None,
                       relative: Optional[int] = None) -> dict:
        """
        Seeks to a specific position in time for a MultiViewer view player.

        Parameters
        ----------
        id: int
            Id of MultiViewer video player.

        absolute: int, optional
            Absolute position in the timeline.

        relative: int, optional
            Relative position from current..

        Returns
        -------
        dict
            Seek response.

        """
        return client.player_seek_to(id=id,
                                     absolute=absolute,
                                     relative=relative)

    @mcp.tool()
    def player_set_bounds(
        id: int,
        x: Optional[int] = None,
        y: Optional[int] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
    ) -> dict:
        """
        Set the bounds and/or position of a MultiViewer video player.

        Parameters
        ----------
        id: int
            Id of a MultiViewer video player.

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
        return client.player_set_bounds(id=id,
                                        x=x,
                                        y=y,
                                        width=width,
                                        height=height)

    @mcp.tool()
    def player_set_volume(id: int, volume: int) -> dict:
        """
        Set the volume of a MultiViewer video player.

        Parameters
        ----------
        id: int
            Id of MultiViewer video player.

        volume: int
            Volume of player from 1 to 100.

        Returns
        -------
        dict
            True if operation is successful.

        """
        return client.player_set_volume(id=id, volume=volume)

    @mcp.tool()
    def player_set_paused(id: int, paused: Optional[bool] = None) -> dict:
        """
        Pauses/unpauses a MultiViewer video player or
        specifies pause state for player.

        Parameters
        ----------
        id: int
            Id of MultiViewer video player.

        paused: bool, optional
            Desired pause state for MultiViewer video player.

        Returns
        -------
        dict
            True if operation is successful.

        """
        return client.player_set_paused(id=id, paused=paused)

    @mcp.tool()
    def player_set_fullscreen(id: int, fullscreen: Optional[bool] = None) -> dict:
        """
        Toggles fullscreen for a MultiViewer video player
        or specifies fullscreen state for player.

        Parameters
        ----------
        id: int
            Id of MultiViewer video player.

        fullscreen: bool, optional
            Desired fullscreen state of player.

        Returns
        -------
        dict
            True if operation is successful.

        """
        return client.player_set_fullscreen(id=id, fullscreen=fullscreen)

    @mcp.tool()
    def player_set_muted(id: int, muted: Optional[bool] = None) -> dict:
        """
        Mutes/unmutes MultiViewer video player or specifies
        muted state for player.

        Parameters
        ----------
        id: int
            Id of MultiViewer video player.

        muted: bool, optional
            Desired muted state of player.

        Returns
        -------
        dict
            True if operation is successful.

        """
        return client.player_set_muted(id=id, muted=muted)

    @mcp.tool()
    def player_set_speedometer_visibility(
        id: int, visible: Optional[bool] = None
    ) -> dict:
        """
        Makes speedometer overlay on MultiViewer player
        visible/invisible or specifies visibility.

        Parameters
        ----------
        id: int
            Id of MultiViewer video player.

        visible: bool, optional
            Visibility state of speedometer of player.

        Returns
        -------
        dict
            True if operation is successful.

        """
        return client.player_set_speedometer_visibility(id=id,
                                                        visible=visible)

    @mcp.tool()
    def player_set_driver_header_mode(id: int,
                                      mode: Optional[str] = None) -> dict:
        """
        Sets the overlay display for a driver onboard MultiViewer vide
        player.

        Parameters
        ----------
        id: int
            Id of MultiViewer video player.

        mode: str, optional
            Desired overlay of the player - can be DRIVER_HEADER, NONE or
            OBC_LIVE_TIMING

        Returns
        -------
        dict
            True if operation is successful.

        """
        return client.player_set_driver_header_mode(id=id,
                                                    mode=mode)

    @mcp.tool()
    def player_set_always_on_top(
        id: int, always_on_top: Optional[bool] = None
    ) -> dict:
        """
        Sets a MultiPlayer video player on/off always on top.

        Parameters
        ----------
        id: int
            Id of MultiViewer video player.

        always_on_top: bool, optional
            Is the player always on top?

        Returns
        -------
        dict
            True if operation is successful.

        """
        return client.player_set_always_on_top(id=id,
                                               always_on_top=always_on_top)

    @mcp.tool()
    def player_sync(id: int) -> dict:
        """
        Synchronizes all players to the timestamp of specified MultiViewer
        video player.

        Parameters
        ----------
        id: int
            Id of MultiViewer video player with which to
            sync all other players.

        Returns
        -------
        dict
            True if operation is successful.

        """
        return client.player_sync(id=id)

    @mcp.tool()
    def player_sync_to_commentary() -> dict:
        """
        Synchronizes all MultiViewer video players to the player
        with a broadcast commentary stream.

        Returns
        -------
        dict
            True if operation is successful.

        """
        return client.player_sync_to_commentary()

    @mcp.tool()
    def player_get_content_id() -> str:
        """
        Retrieve the content_id from the first MultiViewer video player.

        Returns
        -------
        str
            The content_id of the currently playing session.

        """
        players = client.players

        if len(players) > 0:
            return players[0].content_id
        else:
            return "No players are currently active."

    return mcp


# Backward compatibility - create default server instance
client = MultiViewerForF1()
mcp = create_mcp_server()