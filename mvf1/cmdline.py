import click

from mvf1 import MultiViewerForF1
from mvf1 import MultiViewerForF1Error

remote = MultiViewerForF1()

@click.group()
def cli():
    pass


@cli.group(help="Query and control MultiViewerForF1 players.")
def players():
    pass

@players.command(help="List all active MultiViewerForF1 players.")
@click.option('--verbose', is_flag=True, default=False,
              help="Display all player information.")
def ls(verbose):
   players = remote.players

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

@players.command(help="Close all active MultiViewerForF1 players.",
                 name="close")
def players_close():
    players = remote.players
    for player in players:
        click.echo(f"Closing ID {player.id} - {player.title}...")
        player.delete()
    click.echo("Done.")

@players.command(help="Mute all active MultiViewerForF1 players.",
                 name="mute")
def players_mute():
    players = remote.players
    for player in players:
        click.echo(f"Muting ID {player.id} - {player.title}...")
        player.mute()
    click.echo("Done.")

@players.command(help="Pause all active MultiViewerForF1 players.",
                 name="pause")
def players_pause():
    players = remote.players
    for player in players:
        click.echo(f"Pausing ID {player.id} - {player.title}...")
        player.pause()
    click.echo("Done.")

@players.command(help="Synchronize all active MultiViewerForF1 players to the "
                 "player streaming broadcast commentary.",
                 name="sync")
def players_sync():
    click.echo("Syncing all players to broadcast commentary...")
    remote.player_sync_to_commentary()
    click.echo("Done.")

@cli.group(help="Query and control a specific MultiViewerForF1 player.")
@click.option('--id', required=False, type=int)
@click.option('--title', required=False, type=str)
@click.pass_context
def player(ctx, id, title):
    if not id and not title:
        raise click.UsageError("To control a player, pass either an --id or "
                               "--title. To see IDs and Titles, use mvf1 "
                               "players ls")
    ctx.ensure_object(dict)

    if id:
        try:
            ctx.obj['player'] = remote.player(id)
        except MultiViewerForF1Error as e:
            raise click.UsageError(e)
    else:
        players = remote.players

        for player in players:
            if player.title == title:
                ctx.obj['player'] = player
                return
        raise click.UsageError("No player found with title "
                               f"{title}")

@player.command(help="Display information about player.")
@click.option('--verbose', is_flag=True, default=False,
              help="Display all player information.")
@click.pass_context
def query(ctx, verbose):
    player = ctx.obj['player']

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

@player.command(help="Close player",
                name="close")
@click.pass_context
def player_close(ctx):
    player = ctx.obj['player']
    click.echo(f"Closing player ID: {player.id} - {player.title}...")
    player.delete()
    click.echo("Done.")

@player.command(help="Seek to relative or absolute position")
@click.option('--absolute', required=False, type=int)
@click.option('--relative', required=False, type=int)
@click.pass_context
def seek(ctx, absolute, relative):
    if not absolute and not relative:
        raise click.UsageError("To seek a player, pass with an --absolute or "
                               "--relative number of seconds. This can any positive"
                               "or negative integer.")

    player = ctx.obj['player']
    click.echo(f"Seeking player ID {player.id} - {player.title}...")
    player.seek(absolute=absolute, relative=relative)
    click.echo("Done.")

@player.command(help="Adjust position and/or dimensions")
@click.option('--x', required=False, type=int)
@click.option('--y', required=False, type=int)
@click.option('--width', required=False, type=int)
@click.option('--height', required=False, type=int)
@click.pass_context
def set_bounds(ctx, x, y, width, height):
    if not x and not y and not width and not height:
        raise click.UsageError("To adjust position or dimensions of a player, "
                               "pass --x and --y to place the top left corner "
                               "of the player. Pass --width and --height for "
                               "the dimensions of the player.")

    player = ctx.obj['player']
    click.echo(f"Adjusting bounds of player ID {player.id} - "
               f"{player.title}...")
    player.set_bounds(x=x, y=y, width=width, height=height)
    click.echo("Done.")

@player.command(help="Adjust volume")
@click.option('--volume', required=True, type=int)
@click.pass_context
def set_volume(ctx, volume):
    if not volume:
        raise click.UsageError("To adjust volume, pass --volume with an "
                               "integer between 1 and 100.")
    player = ctx.obj['player']
    click.echo(f"Setting volume for player ID {player.id} - "
               f"{player.title}...")
    player.set_volume(volume=volume)
    click.echo("Done.")

@player.command(help="Pause")
@click.pass_context
def pause(ctx):
    player = ctx.obj['player']
    click.echo(f"Pausing player ID {player.id} - {player.title}...")
    player.pause()
    click.echo("Done.")

@player.command(help="Toggle fullscreen")
@click.pass_context
def set_fullscreen(ctx):
    player = ctx.obj['player']
    click.echo(f"Toggling fullscreen for player ID {player.id} - "
               f"{player.title}...")
    player.set_fullscreen()
    click.echo("Done.")

@player.command(help="Mute")
@click.pass_context
def mute(ctx):
    player = ctx.obj['player']
    click.echo(f"Muting player ID {player.id} - {player.title}...")
    player.mute()
    click.echo("Done.")

@player.command(help="Toggle speedometer visibility")
@click.pass_context
def set_speedometer_visibility(ctx):
    player = ctx.obj['player']
    click.echo(f"Toggling speedometer visibility player ID {player.id} - "
               f"{player.title}...")
    player.set_speedometer_visibility()
    click.echo("Done.")

@player.command(help="Synchronize all players to this player's timestamp")
@click.pass_context
def sync(ctx):
    player = ctx.obj['player']
    click.echo(f"Synchronizing all players to player ID {player.id} - "
               f"{player.title}...")
    player.sync()
    click.echo("Done.")

@player.command(help="Switch player's video stream.")
@click.option('--title', required=True, type=str)
@click.pass_context
def switch_stream(ctx, title):
    if not title:
        raise click.UsageError("To switch the stream of a player, pass the "
                               "--title of the desired stream.\n\n"
                               "For example, use INTERNATIONAL for Crofty or "
                               "the three letter acronoym for a driver - "
                               "PER for Sergio Perez.")
    player = ctx.obj['player']
    click.echo(f"Switching stream for player ID {player.id} - {player.title} "
               f"to {title}...")
    player.switch_stream(title)
    click.echo("Done.")
