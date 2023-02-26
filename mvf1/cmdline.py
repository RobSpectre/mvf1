import click

from mvf1 import MultiViewerForF1
from mvf1 import MultiViewerForF1Error

from urllib.error import URLError

remote = MultiViewerForF1()


@click.group()
def cli():
    pass


@cli.group(name="players", help="Query and control MultiViewerForF1 players.")
def mv_players():
    pass


@mv_players.command(help="List all active MultiViewerForF1 players.")
@click.option(
    "--verbose", is_flag=True, default=False, help="Display all player information."
)
def ls(verbose):
    try:
        players = remote.players
    except URLError:
        raise click.UsageError("MultiViewer for F1 is not found. Is the app " "open?")
    except MultiViewerForF1Error as e:
        raise click.UsageError(f"MultiViewer for F1 error: {str(e)}")
    except Exception as e:
        raise click.UsageError(f"Unexpected error: {str(e)}")

    if len(players) == 0:
        raise click.UsageError("No active players found. Is MultiViewerForF1 running?")

    for player in players:
        click.echo(f"ID: {player.id} - Title: {player.title}")
        if verbose:
            click.echo("--------------------------------------------------")
            click.echo(f"State: {player.state}")
            click.echo(f"driverData: {player.driver_data}")
            click.echo(f"streamData: {player.stream_data}")
            click.echo(f"Position: {player.x}, {player.y}")
            click.echo(f"Dimensions: {player.width}, {player.height}")
            click.echo(f"Fullscreen: {player.fullscreen}")
            click.echo(f"Always On Top: {player.always_on_top}")
            click.echo(f"Maintain Aspect Ratio: {player.maintain_aspect_ratio}")


@mv_players.command(help="Close all active MultiViewerForF1 players.", name="close")
def players_close():
    try:
        players = remote.players
    except URLError:
        raise click.UsageError("MultiViewer for F1 is not found. Is the app "
                               "running?")
    except MultiViewerForF1Error as e:
        raise click.UsageError(f"MultiViewer for F1 error: {str(e)}")
    except Exception as e:
        raise click.UsageError(f"Unexpected error: {str(e)}")

    for player in players:
        click.echo(f"Closing ID {player.id} - {player.title}...")
        try:
            player.delete()
        except URLError:
            raise click.UsageError("MultiViewer for F1 not found. Is the app "
                                   "running?")
        except MultiViewerForF1Error as e:
            raise click.UsageError(f"MultiViewer for F1 error: {str(e)}")
        except Exception as e:
            raise click.UsageError(f"Unexpected error: {str(e)}")
    click.echo("Done.")


@mv_players.command(help="Mute all active MultiViewerForF1 players.", name="mute")
def players_mute():
    try:
        players = remote.players
    except URLError:
        raise click.UsageError("MultiViewer for F1 not found. Is the app "
                               "running?")
    except MultiViewerForF1Error as e:
        raise click.UsageError(f"MultiViewer for F1 error: {str(e)}")
    except Exception as e:
        raise click.UsageError(f"Unexpected error: {str(e)}")
    for player in players:
        click.echo(f"Muting ID {player.id} - {player.title}...")
        try:
            player.mute()
        except URLError:
            raise click.UsageError("MultiViewer for F1 not found. Is the app "
                                   "running?")
        except MultiViewerForF1Error as e:
            raise click.UsageError(f"MultiViewer for F1 error: {str(e)}")
        except Exception as e:
            raise click.UsageError(f"Unexpected error: {str(e)}")
    click.echo("Done.")


@mv_players.command(help="Pause all active MultiViewerForF1 players.", name="pause")
def players_pause():
    try:
        players = remote.players
    except URLError:
        raise click.UsageError("MultiViewer for F1 not found. Is the app "
                               "running?")
    except MultiViewerForF1Error as e:
        raise click.UsageError(f"MultiViewer for F1 error: {str(e)}")
    except Exception as e:
        raise click.UsageError(f"Unexpected error: {str(e)}")
    for player in players:
        click.echo(f"Pausing ID {player.id} - {player.title}...")
        try:
            player.pause()
        except URLError:
            raise click.UsageError("MultiViewer for F1 not found. Is the app "
                                   "running?")
        except MultiViewerForF1Error as e:
            raise click.UsageError(f"MultiViewer for F1 error: {str(e)}")
        except Exception as e:
            raise click.UsageError(f"Unexpected error: {str(e)}")
    click.echo("Done.")


@mv_players.command(
    help="Synchronize all active MultiViewerForF1 players to the "
    "player streaming broadcast commentary.",
    name="sync",
)
def players_sync():
    click.echo("Syncing all players to broadcast commentary...")
    try:
        remote.player_sync_to_commentary()
    except URLError:
        raise click.UsageError("MultiViewer for F1 not found. Is the app "
                               "running?")
    except MultiViewerForF1Error as e:
        raise click.UsageError(f"MultiViewer for F1 error: {str(e)}")
    except Exception as e:
        raise click.UsageError(f"Unexpected error: {str(e)}")
    click.echo("Done.")


@cli.group(name="player", help="Query and control a specific MultiViewerForF1 player.")
@click.option("--id", required=False, type=int)
@click.option("--title", required=False, type=str)
@click.pass_context
def mv_player(ctx, id, title):
    ctx.ensure_object(dict)

    if id:
        try:
            ctx.obj["player"] = remote.player(id)
        except URLError:
            raise click.UsageError("MultiViewer for F1 not found. Is the app "
                                   "running?")
        except MultiViewerForF1Error as e:
            raise click.UsageError(f"MultiViewer for F1 error: {str(e)}")
        except Exception as e:
            raise click.UsageError(f"Unexpected error: {str(e)}")
    else:
        try:
            players = remote.players
        except URLError:
            raise click.UsageError("MultiViewer for F1 not found. Is the app "
                                   "running?")
        except MultiViewerForF1Error as e:
            raise click.UsageError(f"MultiViewer for F1 error: {str(e)}")
        except Exception as e:
            raise click.UsageError(f"Unexpected error: {str(e)}")

        for player in players:
            if player.title == title:
                ctx.obj["player"] = player
                return
        raise click.UsageError("No player found with title " f"{title}")


@mv_player.command(help="Display information about player.")
@click.option(
    "--verbose", is_flag=True, default=False, help="Display all player information."
)
@click.pass_context
def query(ctx, verbose):
    player = ctx.obj["player"]

    click.echo(f"ID: {player.id} - Title: {player.title}")
    if verbose:
        click.echo("--------------------------------------------------")
        click.echo(f"State: {player.state}")
        click.echo(f"driverData: {player.driver_data}")
        click.echo(f"streamData: {player.stream_data}")
        click.echo(f"Position: {player.x}, {player.y}")
        click.echo(f"Dimensions: {player.width}, {player.height}")
        click.echo(f"Fullscreen: {player.fullscreen}")
        click.echo(f"Always On Top: {player.always_on_top}")
        click.echo(f"Maintain Aspect Ratio: {player.maintain_aspect_ratio}")


@mv_player.command(help="Close player", name="close")
@click.pass_context
def player_close(ctx):
    player = ctx.obj["player"]
    click.echo(f"Closing player ID: {player.id} - {player.title}...")
    try:
        player.delete()
    except URLError:
        raise click.UsageError("MultiViewer for F1 not found. Is the app "
                               "running?")
    except MultiViewerForF1Error as e:
        raise click.UsageError(f"MultiViewer for F1 error: {str(e)}")
    except Exception as e:
        raise click.UsageError(f"Unexpected error: {str(e)}")
    click.echo("Done.")


@mv_player.command(help="Seek to relative or absolute position")
@click.option("--absolute", required=False, type=int)
@click.option("--relative", required=False, type=int)
@click.pass_context
def seek(ctx, absolute, relative):
    if not absolute and not relative:
        raise click.UsageError(
            "To seek a player, pass with an --absolute or "
            "--relative number of seconds. This can any positive"
            "or negative integer."
        )

    player = ctx.obj["player"]
    click.echo(f"Seeking player ID {player.id} - {player.title}...")
    try:
        player.seek(absolute=absolute, relative=relative)
    except URLError:
        raise click.UsageError("MultiViewer for F1 not found. Is the app "
                               "running?")
    except MultiViewerForF1Error as e:
        raise click.UsageError(f"MultiViewer for F1 error: {str(e)}")
    except Exception as e:
        raise click.UsageError(f"Unexpected error: {str(e)}")
    click.echo("Done.")


@mv_player.command(help="Adjust position and/or dimensions")
@click.option("--x", required=False, type=int)
@click.option("--y", required=False, type=int)
@click.option("--width", required=False, type=int)
@click.option("--height", required=False, type=int)
@click.pass_context
def set_bounds(ctx, x, y, width, height):
    player = ctx.obj["player"]
    click.echo(f"Adjusting bounds of player ID {player.id} - " f"{player.title}...")
    try:
        player.set_bounds(x=x, y=y, width=width, height=height)
    except URLError:
        raise click.UsageError("MultiViewer for F1 not found. Is the app "
                               "running?")
    except MultiViewerForF1Error as e:
        raise click.UsageError(f"MultiViewer for F1 error: {str(e)}")
    except Exception as e:
        raise click.UsageError(f"Unexpected error: {str(e)}")
    click.echo("Done.")


@mv_player.command(help="Adjust volume")
@click.option("--volume", required=True, type=int)
@click.pass_context
def set_volume(ctx, volume):
    player = ctx.obj["player"]
    click.echo(f"Setting volume for player ID {player.id} - " f"{player.title}...")
    try:
        player.set_volume(volume=volume)
    except URLError:
        raise click.UsageError("MultiViewer for F1 not found. Is the app "
                               "running?")
    except MultiViewerForF1Error as e:
        raise click.UsageError(f"MultiViewer for F1 error: {str(e)}")
    except Exception as e:
        raise click.UsageError(f"Unexpected error: {str(e)}")
    click.echo("Done.")


@mv_player.command(help="Pause")
@click.pass_context
def pause(ctx):
    player = ctx.obj["player"]
    click.echo(f"Pausing player ID {player.id} - {player.title}...")
    try:
        player.pause()
    except URLError:
        raise click.UsageError("MultiViewer for F1 not found. Is the app "
                               "running?")
    except MultiViewerForF1Error as e:
        raise click.UsageError(f"MultiViewer for F1 error: {str(e)}")
    except Exception as e:
        raise click.UsageError(f"Unexpected error: {str(e)}")
    click.echo("Done.")


@mv_player.command(help="Toggle fullscreen")
@click.pass_context
def set_fullscreen(ctx):
    player = ctx.obj["player"]
    click.echo(f"Toggling fullscreen for player ID {player.id} - " f"{player.title}...")
    try:
        player.set_fullscreen()
    except URLError:
        raise click.UsageError("MultiViewer for F1 not found. Is the app "
                               "running?")
    except MultiViewerForF1Error as e:
        raise click.UsageError(f"MultiViewer for F1 error: {str(e)}")
    except Exception as e:
        raise click.UsageError(f"Unexpected error: {str(e)}")
    click.echo("Done.")


@mv_player.command(help="Mute")
@click.pass_context
def mute(ctx):
    player = ctx.obj["player"]
    click.echo(f"Muting player ID {player.id} - {player.title}...")
    try:
        player.mute()
    except URLError:
        raise click.UsageError("MultiViewer for F1 not found. Is the app "
                               "running?")
    except MultiViewerForF1Error as e:
        raise click.UsageError(f"MultiViewer for F1 error: {str(e)}")
    except Exception as e:
        raise click.UsageError(f"Unexpected error: {str(e)}")
    click.echo("Done.")


@mv_player.command(help="Toggle speedometer visibility")
@click.pass_context
def set_speedometer_visibility(ctx):
    player = ctx.obj["player"]
    click.echo(
        f"Toggling speedometer visibility player ID {player.id} - " f"{player.title}..."
    )
    try:
        player.set_speedometer_visibility()
    except URLError:
        raise click.UsageError("MultiViewer for F1 not found. Is the app "
                               "running?")
    except MultiViewerForF1Error as e:
        raise click.UsageError(f"MultiViewer for F1 error: {str(e)}")
    except Exception as e:
        raise click.UsageError(f"Unexpected error: {str(e)}")
    click.echo("Done.")


@mv_player.command(help="Synchronize all players to this player's timestamp")
@click.pass_context
def sync(ctx):
    player = ctx.obj["player"]
    click.echo(
        f"Synchronizing all players to player ID {player.id} - " f"{player.title}..."
    )
    try:
        player.sync()
    except URLError:
        raise click.UsageError("MultiViewer for F1 not found. Is the app "
                               "running?")
    except MultiViewerForF1Error as e:
        raise click.UsageError(f"MultiViewer for F1 error: {str(e)}")
    except Exception as e:
        raise click.UsageError(f"Unexpected error: {str(e)}")
    click.echo("Done.")


@mv_player.command(help="Switch player's video stream.")
@click.option("--title", required=True, type=str)
@click.pass_context
def switch_stream(ctx, title):
    player = ctx.obj["player"]
    click.echo(
        f"Switching stream for player ID {player.id} - {player.title} " f"to {title}..."
    )
    try:
        player.switch_stream(title)
    except URLError:
        raise click.UsageError("MultiViewer for F1 not found. Is the app "
                               "running?")
    except MultiViewerForF1Error as e:
        raise click.UsageError(f"MultiViewer for F1 error: {str(e)}")
    except Exception as e:
        raise click.UsageError(f"Unexpected error: {str(e)}")
    click.echo("Done.")
