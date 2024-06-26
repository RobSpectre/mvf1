import sgqlc.types


mvf1_schema = sgqlc.types.Schema()


__docformat__ = 'markdown'


########################################################################
# Scalars and Enumerations
########################################################################
class AlwaysOnTopLevel(sgqlc.types.Enum):
    '''Level for always on top mode  See
    https://developer.apple.com/documentation/appkit/nswindow/level

    Enumeration Choices:

    * `FLOATING`None
    * `MAIN_MENU`None
    * `MODAL_PANEL`None
    * `NORMAL`None
    * `POP_UP_MENU`None
    * `SCREEN_SAVER`None
    * `STATUS`None
    * `TORN_OFF_MENU`None
    '''
    __schema__ = mvf1_schema
    __choices__ = ('FLOATING', 'MAIN_MENU', 'MODAL_PANEL', 'NORMAL', 'POP_UP_MENU', 'SCREEN_SAVER', 'STATUS', 'TORN_OFF_MENU')


class BigInt(sgqlc.types.Scalar):
    '''Integer represented as a base-10 string'''
    __schema__ = mvf1_schema


Boolean = sgqlc.types.Boolean

class DriverHeaderMode(sgqlc.types.Enum):
    '''The driver header mode for on-board players

    Enumeration Choices:

    * `DRIVER_HEADER`: Show the driver's headshot and TLA
    * `NONE`: Show nothing at all
    * `OBC_LIVE_TIMING`: Show live timing data for the driver (when
      live timing is available)
    '''
    __schema__ = mvf1_schema
    __choices__ = ('DRIVER_HEADER', 'NONE', 'OBC_LIVE_TIMING')


Float = sgqlc.types.Float

ID = sgqlc.types.ID

Int = sgqlc.types.Int

class JSONObject(sgqlc.types.Scalar):
    '''Object with arbitrary, untyped data'''
    __schema__ = mvf1_schema


class PlayerType(sgqlc.types.Enum):
    '''The player type

    Enumeration Choices:

    * `ADDITIONAL`: Additional stream, such as International, F1 Live,
      Data channel or Driver tracker
    * `OBC`: On-board camera, for drivers
    '''
    __schema__ = mvf1_schema
    __choices__ = ('ADDITIONAL', 'OBC')


String = sgqlc.types.String

class SubscriptionType(sgqlc.types.Enum):
    '''The type of subscription

    Enumeration Choices:

    * `F1TV_ACCESS`None
    * `F1TV_PRO`None
    * `F1_ACCESS`None
    '''
    __schema__ = mvf1_schema
    __choices__ = ('F1TV_ACCESS', 'F1TV_PRO', 'F1_ACCESS')



########################################################################
# Input Objects
########################################################################
class PlayerCreateInput(sgqlc.types.Input):
    '''The input for creating a player'''
    __schema__ = mvf1_schema
    __field_names__ = ('content_id', 'channel_id', 'driver_tla', 'driver_number', 'stream_title', 'bounds', 'fullscreen', 'always_on_top', 'maintain_aspect_ratio')
    content_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='contentId')
    '''The contentId for the player'''

    channel_id = sgqlc.types.Field(Int, graphql_name='channelId')
    '''The channelId (if applicable) for this player'''

    driver_tla = sgqlc.types.Field(String, graphql_name='driverTla')
    '''The TLA (Three-Letter-Acronym) for the driver (if applicable) for
    this player  > Note: this can be used instead of channelId
    '''

    driver_number = sgqlc.types.Field(Int, graphql_name='driverNumber')
    '''The driver number for the driver (if applicable) for this player
    > Note: this can be used instead of channelId
    '''

    stream_title = sgqlc.types.Field(String, graphql_name='streamTitle')
    '''The title of the stream (if applicable) for this player  > Note:
    this can be used instead of channelId
    '''

    bounds = sgqlc.types.Field('RectangleInput', graphql_name='bounds')
    '''The bounds for this window'''

    fullscreen = sgqlc.types.Field(Boolean, graphql_name='fullscreen')
    '''Whether the player should be fullscreen or not'''

    always_on_top = sgqlc.types.Field(Boolean, graphql_name='alwaysOnTop')
    '''Whether the player should be always on top or not'''

    maintain_aspect_ratio = sgqlc.types.Field(Boolean, graphql_name='maintainAspectRatio')
    '''Whether the player should maintain aspect ratio or not'''



class RectangleInput(sgqlc.types.Input):
    '''A rectangle input, with the dimensions and position'''
    __schema__ = mvf1_schema
    __field_names__ = ('x', 'y', 'width', 'height')
    x = sgqlc.types.Field(Int, graphql_name='x')
    '''The x position of the rectangle'''

    y = sgqlc.types.Field(Int, graphql_name='y')
    '''The y position of the rectangle'''

    width = sgqlc.types.Field(Int, graphql_name='width')
    '''The width of the rectangle'''

    height = sgqlc.types.Field(Int, graphql_name='height')
    '''The height of the rectangle'''




########################################################################
# Output Objects and Interfaces
########################################################################
class F1LiveTimingClock(sgqlc.types.Type):
    '''Clock information for the live timing'''
    __schema__ = mvf1_schema
    __field_names__ = ('paused', 'system_time', 'track_time', 'live_timing_start_time')
    paused = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='paused')
    '''Whether or not the clock is paused'''

    system_time = sgqlc.types.Field(sgqlc.types.non_null(BigInt), graphql_name='systemTime')
    '''The timestamp on the host computer that represents the `trackTime`'''

    track_time = sgqlc.types.Field(sgqlc.types.non_null(BigInt), graphql_name='trackTime')
    '''The timestamp at the track, at the time on the host computer'''

    live_timing_start_time = sgqlc.types.Field(sgqlc.types.non_null(BigInt), graphql_name='liveTimingStartTime')
    '''Live timing start time, indicating the first recorded event's
    timestamp (track time)
    '''



class F1LiveTimingState(sgqlc.types.Type):
    '''F1 live timing state'''
    __schema__ = mvf1_schema
    __field_names__ = ('archive_status', 'audio_streams', 'car_data', 'championship_prediction', 'content_streams', 'driver_list', 'extrapolated_clock', 'heartbeat', 'lap_count', 'lap_series', 'pit_lane_time_collection', 'position', 'race_control_messages', 'session_data', 'session_info', 'session_status', 'team_radio', 'timing_app_data', 'timing_data', 'timing_stats', 'top_three', 'track_status', 'weather_data', 'weather_data_series')
    archive_status = sgqlc.types.Field(JSONObject, graphql_name='ArchiveStatus')
    '''The status of the live timing archive, used for replay live timing'''

    audio_streams = sgqlc.types.Field(JSONObject, graphql_name='AudioStreams')
    '''Available audio commentary streams'''

    car_data = sgqlc.types.Field(JSONObject, graphql_name='CarData')
    '''Car telemetry data, speed, throttle, brake, gear, RPM, DRS'''

    championship_prediction = sgqlc.types.Field(JSONObject, graphql_name='ChampionshipPrediction')
    '''Live championship standings, available for sessions where points
    are being awarded
    '''

    content_streams = sgqlc.types.Field(JSONObject, graphql_name='ContentStreams')
    '''Text-based content streams (via ScribbleLive) and audio commentary'''

    driver_list = sgqlc.types.Field(JSONObject, graphql_name='DriverList')
    '''List of all participating drivers with basic information'''

    extrapolated_clock = sgqlc.types.Field(JSONObject, graphql_name='ExtrapolatedClock')
    '''Extrapolated session clock  The extrapolated session clock returns
    the time in UTC (via the `Utc` field) and the remaining time for
    this session (via the `Extrapolating` field), and if the clock is
    still extrapolating (via the `Extrapolating` field). You can use
    this data, along with the `liveTimingClock` field on the root
    query, to calculate the time remaining in the session.
    '''

    heartbeat = sgqlc.types.Field(JSONObject, graphql_name='Heartbeat')
    '''Heartbeats from the live timing server'''

    lap_count = sgqlc.types.Field(JSONObject, graphql_name='LapCount')
    '''Lap count, for sessions with a schedule number of laps'''

    lap_series = sgqlc.types.Field(JSONObject, graphql_name='LapSeries')
    '''Time-series data per lap for each driver's position during the
    session
    '''

    pit_lane_time_collection = sgqlc.types.Field(JSONObject, graphql_name='PitLaneTimeCollection')
    '''Current or recent pit-stop timing data'''

    position = sgqlc.types.Field(JSONObject, graphql_name='Position')
    '''GPS positioning for cars and safety cars'''

    race_control_messages = sgqlc.types.Field(JSONObject, graphql_name='RaceControlMessages')
    '''Messages sent by FIA race control'''

    session_data = sgqlc.types.Field(JSONObject, graphql_name='SessionData')
    '''Simple session data, containing session status and start times for
    multi-part sessions (like Qualifying)
    '''

    session_info = sgqlc.types.Field(JSONObject, graphql_name='SessionInfo')
    '''Session information, including session type, circuit, official
    names and the scheduled start time
    '''

    session_status = sgqlc.types.Field(JSONObject, graphql_name='SessionStatus')
    '''The current session status (for which a time-series is available
    in the `SessionData` topic)
    '''

    team_radio = sgqlc.types.Field(JSONObject, graphql_name='TeamRadio')
    '''Team radio message captures'''

    timing_app_data = sgqlc.types.Field(JSONObject, graphql_name='TimingAppData')
    '''Timing data for tyre stints, grid start positions, including tyre
    compound, best time set on it and the amount of laps run on it
    '''

    timing_data = sgqlc.types.Field(JSONObject, graphql_name='TimingData')
    '''Most timing data available, including lap times, sector times,
    intervals/gaps, pitstop status, speed traps and number of laps run
    '''

    timing_stats = sgqlc.types.Field(JSONObject, graphql_name='TimingStats')
    '''Statistics for the current session, best lap times, best sectors,
    best speeds
    '''

    top_three = sgqlc.types.Field(JSONObject, graphql_name='TopThree')
    '''Basic information about the top-three drivers in this session'''

    track_status = sgqlc.types.Field(JSONObject, graphql_name='TrackStatus')
    '''The track status, which changes when yellow or red flags are out'''

    weather_data = sgqlc.types.Field(JSONObject, graphql_name='WeatherData')
    '''Current weather data'''

    weather_data_series = sgqlc.types.Field(JSONObject, graphql_name='WeatherDataSeries')
    '''Historic weather data, for the current session'''



class FIAWECLiveTimingState(sgqlc.types.Type):
    '''FIA WEC live timing state'''
    __schema__ = mvf1_schema
    __field_names__ = ('entries', 'referential', 'params', 'flags', 'best_sectors', 'race_control', 'laps', 'stints')
    entries = sgqlc.types.Field(JSONObject, graphql_name='entries')
    '''The race entries, which are the cars competing, including the
    drivers of that car, and other information
    '''

    referential = sgqlc.types.Field(JSONObject, graphql_name='referential')
    '''Referential data, which includes the entries, driver data,
    category data, information about the sessions and the race/brands
    '''

    params = sgqlc.types.Field(JSONObject, graphql_name='params')
    '''Information related to the current session, and track data such as
    weather, flag state, etc.
    '''

    flags = sgqlc.types.Field(JSONObject, graphql_name='flags')
    '''Any flags that are currently active'''

    best_sectors = sgqlc.types.Field(JSONObject, graphql_name='best_sectors')
    '''Best sectors overall'''

    race_control = sgqlc.types.Field(JSONObject, graphql_name='race_control')
    '''Race control messages'''

    laps = sgqlc.types.Field(JSONObject, graphql_name='laps')
    '''Lap-by-lap data for each car'''

    stints = sgqlc.types.Field(JSONObject, graphql_name='stints')
    '''Stint data for each car'''



class LiveTimingClock(sgqlc.types.Type):
    '''Clock information for the live timing'''
    __schema__ = mvf1_schema
    __field_names__ = ('paused', 'system_time', 'track_time', 'live_timing_start_time')
    paused = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='paused')
    '''Whether or not the clock is paused'''

    system_time = sgqlc.types.Field(sgqlc.types.non_null(BigInt), graphql_name='systemTime')
    '''The timestamp on the host computer that represents the `trackTime`'''

    track_time = sgqlc.types.Field(sgqlc.types.non_null(BigInt), graphql_name='trackTime')
    '''The timestamp at the track, at the time on the host computer'''

    live_timing_start_time = sgqlc.types.Field(sgqlc.types.non_null(BigInt), graphql_name='liveTimingStartTime')
    '''Live timing start time, indicating the first recorded event's
    timestamp (track time)
    '''



class LiveTimingState(sgqlc.types.Type):
    '''F1 live timing state'''
    __schema__ = mvf1_schema
    __field_names__ = ('archive_status', 'audio_streams', 'car_data', 'championship_prediction', 'content_streams', 'driver_list', 'extrapolated_clock', 'heartbeat', 'lap_count', 'lap_series', 'pit_lane_time_collection', 'position', 'race_control_messages', 'session_data', 'session_info', 'session_status', 'team_radio', 'timing_app_data', 'timing_data', 'timing_stats', 'top_three', 'track_status', 'weather_data', 'weather_data_series')
    archive_status = sgqlc.types.Field(JSONObject, graphql_name='ArchiveStatus')
    '''The status of the live timing archive, used for replay live timing'''

    audio_streams = sgqlc.types.Field(JSONObject, graphql_name='AudioStreams')
    '''Available audio commentary streams'''

    car_data = sgqlc.types.Field(JSONObject, graphql_name='CarData')
    '''Car telemetry data, speed, throttle, brake, gear, RPM, DRS'''

    championship_prediction = sgqlc.types.Field(JSONObject, graphql_name='ChampionshipPrediction')
    '''Live championship standings, available for sessions where points
    are being awarded
    '''

    content_streams = sgqlc.types.Field(JSONObject, graphql_name='ContentStreams')
    '''Text-based content streams (via ScribbleLive) and audio commentary'''

    driver_list = sgqlc.types.Field(JSONObject, graphql_name='DriverList')
    '''List of all participating drivers with basic information'''

    extrapolated_clock = sgqlc.types.Field(JSONObject, graphql_name='ExtrapolatedClock')
    '''Extrapolated session clock  The extrapolated session clock returns
    the time in UTC (via the `Utc` field) and the remaining time for
    this session (via the `Extrapolating` field), and if the clock is
    still extrapolating (via the `Extrapolating` field). You can use
    this data, along with the `liveTimingClock` field on the root
    query, to calculate the time remaining in the session.
    '''

    heartbeat = sgqlc.types.Field(JSONObject, graphql_name='Heartbeat')
    '''Heartbeats from the live timing server'''

    lap_count = sgqlc.types.Field(JSONObject, graphql_name='LapCount')
    '''Lap count, for sessions with a schedule number of laps'''

    lap_series = sgqlc.types.Field(JSONObject, graphql_name='LapSeries')
    '''Time-series data per lap for each driver's position during the
    session
    '''

    pit_lane_time_collection = sgqlc.types.Field(JSONObject, graphql_name='PitLaneTimeCollection')
    '''Current or recent pit-stop timing data'''

    position = sgqlc.types.Field(JSONObject, graphql_name='Position')
    '''GPS positioning for cars and safety cars'''

    race_control_messages = sgqlc.types.Field(JSONObject, graphql_name='RaceControlMessages')
    '''Messages sent by FIA race control'''

    session_data = sgqlc.types.Field(JSONObject, graphql_name='SessionData')
    '''Simple session data, containing session status and start times for
    multi-part sessions (like Qualifying)
    '''

    session_info = sgqlc.types.Field(JSONObject, graphql_name='SessionInfo')
    '''Session information, including session type, circuit, official
    names and the scheduled start time
    '''

    session_status = sgqlc.types.Field(JSONObject, graphql_name='SessionStatus')
    '''The current session status (for which a time-series is available
    in the `SessionData` topic)
    '''

    team_radio = sgqlc.types.Field(JSONObject, graphql_name='TeamRadio')
    '''Team radio message captures'''

    timing_app_data = sgqlc.types.Field(JSONObject, graphql_name='TimingAppData')
    '''Timing data for tyre stints, grid start positions, including tyre
    compound, best time set on it and the amount of laps run on it
    '''

    timing_data = sgqlc.types.Field(JSONObject, graphql_name='TimingData')
    '''Most timing data available, including lap times, sector times,
    intervals/gaps, pitstop status, speed traps and number of laps run
    '''

    timing_stats = sgqlc.types.Field(JSONObject, graphql_name='TimingStats')
    '''Statistics for the current session, best lap times, best sectors,
    best speeds
    '''

    top_three = sgqlc.types.Field(JSONObject, graphql_name='TopThree')
    '''Basic information about the top-three drivers in this session'''

    track_status = sgqlc.types.Field(JSONObject, graphql_name='TrackStatus')
    '''The track status, which changes when yellow or red flags are out'''

    weather_data = sgqlc.types.Field(JSONObject, graphql_name='WeatherData')
    '''Current weather data'''

    weather_data_series = sgqlc.types.Field(JSONObject, graphql_name='WeatherDataSeries')
    '''Historic weather data, for the current session'''



class Mutation(sgqlc.types.Type):
    __schema__ = mvf1_schema
    __field_names__ = ('version', 'player_create', 'player_delete', 'player_set_fullscreen', 'player_set_always_on_top', 'player_set_bounds', 'player_set_volume', 'player_set_paused', 'player_set_muted', 'player_seek_to', 'player_sync', 'player_set_speedometer_visibility', 'player_set_driver_header_mode')
    version = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='version')
    '''Get the version of the app'''

    player_create = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='playerCreate', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(PlayerCreateInput), graphql_name='input', default=None)),
))
    )
    '''Create a new player  Returns the ID of the created player

    Arguments:

    * `input` (`PlayerCreateInput!`): Input object for this player
    '''

    player_delete = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='playerDelete', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    '''Close a player

    Arguments:

    * `id` (`ID!`): The browserWindowId of the player
    '''

    player_set_fullscreen = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='playerSetFullscreen', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
        ('fullscreen', sgqlc.types.Arg(Boolean, graphql_name='fullscreen', default=None)),
))
    )
    '''Control the fullscreen state of a player  Returns the new
    fullscreen state

    Arguments:

    * `id` (`ID!`): The browserWindowId of the player
    * `fullscreen` (`Boolean`): Whether the player should be
      fullscreen or not, if not set the player will toggle fullscreen
    '''

    player_set_always_on_top = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='playerSetAlwaysOnTop', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
        ('always_on_top', sgqlc.types.Arg(Boolean, graphql_name='alwaysOnTop', default=None)),
        ('level', sgqlc.types.Arg(AlwaysOnTopLevel, graphql_name='level', default=None)),
))
    )
    '''Control the alwaysOnTop state of a player  Returns the new
    alwaysOnTop state

    Arguments:

    * `id` (`ID!`): The browserWindowId of the player
    * `always_on_top` (`Boolean`): Whether the player should be
      alwaysOnTop or not, if not set the player will toggle
      alwaysOnTop
    * `level` (`AlwaysOnTopLevel`): The level of alwaysOnTop, defaults
      to "floating"
    '''

    player_set_bounds = sgqlc.types.Field(sgqlc.types.non_null('Rectangle'), graphql_name='playerSetBounds', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
        ('bounds', sgqlc.types.Arg(sgqlc.types.non_null(RectangleInput), graphql_name='bounds', default=None)),
))
    )
    '''Set the bounds of a player

    Arguments:

    * `id` (`ID!`): The browserWindowId of the player
    * `bounds` (`RectangleInput!`): The new bounds of the player, any
      values that are not specified will remain unchanged
    '''

    player_set_volume = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='playerSetVolume', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
        ('volume', sgqlc.types.Arg(sgqlc.types.non_null(Float), graphql_name='volume', default=None)),
))
    )
    '''Set volume of a player

    Arguments:

    * `id` (`ID!`): The browserWindowId of the player
    * `volume` (`Float!`): The volume of the player (0-100)
    '''

    player_set_paused = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='playerSetPaused', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
        ('paused', sgqlc.types.Arg(Boolean, graphql_name='paused', default=None)),
))
    )
    '''Play/pause a player  Returns the new paused state

    Arguments:

    * `id` (`ID!`): The browserWindowId of the player
    * `paused` (`Boolean`): Whether the player should be paused or
      not, if not set the player will toggle play/paused state
    '''

    player_set_muted = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='playerSetMuted', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
        ('muted', sgqlc.types.Arg(Boolean, graphql_name='muted', default=None)),
))
    )
    '''Mute/unmute a player  Returns the new muted state

    Arguments:

    * `id` (`ID!`): The browserWindowId of the player
    * `muted` (`Boolean`): Whether the player should be muted or not,
      if not set the player will toggle muted/unmuted state
    '''

    player_seek_to = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='playerSeekTo', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
        ('absolute', sgqlc.types.Arg(Float, graphql_name='absolute', default=None)),
        ('relative', sgqlc.types.Arg(Float, graphql_name='relative', default=None)),
))
    )
    '''Seek a player  Requires either `absolute` or `relative` to be set
    > Note: This doesn't work for live players  Returns the seeked
    time

    Arguments:

    * `id` (`ID!`): The browserWindowId of the player
    * `absolute` (`Float`): The timestamp to seek to
    * `relative` (`Float`): The relative amount to seek, negative
      values seek backwards and positive values seek forwards
    '''

    player_sync = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='playerSync', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    '''Sync other players to a player  Returns `true` if the sync was
    successful

    Arguments:

    * `id` (`ID!`): The browserWindowId of the player
    '''

    player_set_speedometer_visibility = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='playerSetSpeedometerVisibility', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
        ('visible', sgqlc.types.Arg(Boolean, graphql_name='visible', default=None)),
))
    )
    '''Control the visibility of the driver speedometer

    Arguments:

    * `id` (`ID!`): The browserWindowId of the player
    * `visible` (`Boolean`): The visibility of the speedometer, if not
      set the speedometer will toggle visibility
    '''

    player_set_driver_header_mode = sgqlc.types.Field(sgqlc.types.non_null(DriverHeaderMode), graphql_name='playerSetDriverHeaderMode', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
        ('mode', sgqlc.types.Arg(sgqlc.types.non_null(DriverHeaderMode), graphql_name='mode', default=None)),
))
    )
    '''Set the driver header mode for on-board players

    Arguments:

    * `id` (`ID!`): The browserWindowId of the player
    * `mode` (`DriverHeaderMode!`): The driver header mode
    '''



class Player(sgqlc.types.Type):
    '''A player object'''
    __schema__ = mvf1_schema
    __field_names__ = ('id', 'type', 'state', 'driver_data', 'stream_data', 'bounds', 'fullscreen', 'always_on_top', 'maintain_aspect_ratio')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    '''The browserWindowId of the player'''

    type = sgqlc.types.Field(sgqlc.types.non_null(PlayerType), graphql_name='type')
    '''The player type'''

    state = sgqlc.types.Field('PlayerState', graphql_name='state')
    '''The player state'''

    driver_data = sgqlc.types.Field('PlayerDriverData', graphql_name='driverData')
    '''If this is a player of type OBC, this will contain the available
    driver data
    '''

    stream_data = sgqlc.types.Field('PlayerStreamData', graphql_name='streamData')
    '''The stream metadata for this player'''

    bounds = sgqlc.types.Field(sgqlc.types.non_null('Rectangle'), graphql_name='bounds')
    '''The bounds of the player'''

    fullscreen = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='fullscreen')
    '''Whether the player is fullscreen or not'''

    always_on_top = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='alwaysOnTop')
    '''Whether the player is always on top or not'''

    maintain_aspect_ratio = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='maintainAspectRatio')
    '''Whether the player maintains aspect ratio or not'''



class PlayerDriverData(sgqlc.types.Type):
    '''Driver metadata for a player'''
    __schema__ = mvf1_schema
    __field_names__ = ('driver_number', 'tla', 'first_name', 'last_name', 'team_name')
    driver_number = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='driverNumber')
    '''The driver's driver number'''

    tla = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='tla')
    '''The drivers TLA (Three-Letter-Acronym)'''

    first_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='firstName')
    '''The driver's first name'''

    last_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='lastName')
    '''The driver's last name'''

    team_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='teamName')
    '''The constructor's name'''



class PlayerState(sgqlc.types.Type):
    '''The player state'''
    __schema__ = mvf1_schema
    __field_names__ = ('ts', 'paused', 'muted', 'volume', 'live', 'current_time', 'interpolated_current_time')
    ts = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='ts')
    '''The UNIX timestamp when the player state was last updated'''

    paused = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='paused')
    '''Whether the player is paused or not'''

    muted = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='muted')
    '''Whether the player is muted or not'''

    volume = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='volume')
    '''The player's volume (0-100)'''

    live = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='live')
    '''Whether the player is live or not'''

    current_time = sgqlc.types.Field(Float, graphql_name='currentTime')
    '''The current time of the player, at the time it was last updated'''

    interpolated_current_time = sgqlc.types.Field(Float, graphql_name='interpolatedCurrentTime')
    '''The interpolated current time of the player'''



class PlayerStreamData(sgqlc.types.Type):
    '''Stream metadata for players'''
    __schema__ = mvf1_schema
    __field_names__ = ('content_id', 'meeting_key', 'session_key', 'channel_id', 'title')
    content_id = sgqlc.types.Field(ID, graphql_name='contentId')
    '''The contentId for this stream'''

    meeting_key = sgqlc.types.Field(String, graphql_name='meetingKey')
    '''The meeting key for this stream (if part of a meeting)'''

    session_key = sgqlc.types.Field(String, graphql_name='sessionKey')
    '''The session key for this stream (if part of a meeting)'''

    channel_id = sgqlc.types.Field(Int, graphql_name='channelId')
    '''If part of a content container with multiple additional streams,
    the ID of the channel
    '''

    title = sgqlc.types.Field(String, graphql_name='title')
    '''The stream's title'''



class Query(sgqlc.types.Type):
    __schema__ = mvf1_schema
    __field_names__ = ('version', 'system_info', 'players', 'player', 'live_timing_state', 'live_timing_clock', 'f1_live_timing_state', 'f1_live_timing_clock', 'fiawec_live_timing_state', 'active_subscriptions')
    version = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='version')
    '''Get the version of the app'''

    system_info = sgqlc.types.Field(sgqlc.types.non_null('SystemInfo'), graphql_name='systemInfo')
    '''Basic system information (platform and CPU architecture)'''

    players = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Player))), graphql_name='players')
    '''Get all open players'''

    player = sgqlc.types.Field(sgqlc.types.non_null(Player), graphql_name='player', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    '''Get a player by ID

    Arguments:

    * `id` (`ID!`)None
    '''

    live_timing_state = sgqlc.types.Field(LiveTimingState, graphql_name='liveTimingState')
    '''Get the live timing state'''

    live_timing_clock = sgqlc.types.Field(LiveTimingClock, graphql_name='liveTimingClock')
    '''Get the clock information for the live timing (for session clock
    etc.)
    '''

    f1_live_timing_state = sgqlc.types.Field(F1LiveTimingState, graphql_name='f1LiveTimingState')
    '''Get the F1 live timing state'''

    f1_live_timing_clock = sgqlc.types.Field(F1LiveTimingClock, graphql_name='f1LiveTimingClock')
    '''Get the clock information for the F1 live timing (for session
    clock etc.)
    '''

    fiawec_live_timing_state = sgqlc.types.Field(FIAWECLiveTimingState, graphql_name='fiawecLiveTimingState')
    '''Get the FIA WEC live timing state'''

    active_subscriptions = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('Subscription'))), graphql_name='activeSubscriptions')
    '''Active subscriptions for the current user'''



class Rectangle(sgqlc.types.Type):
    '''A rectangle, with dimensions and position'''
    __schema__ = mvf1_schema
    __field_names__ = ('x', 'y', 'width', 'height')
    x = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='x')
    '''The x position of the rectangle'''

    y = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='y')
    '''The y position of the rectangle'''

    width = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='width')
    '''The width of the rectangle'''

    height = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='height')
    '''The height of the rectangle'''



class Subscription(sgqlc.types.Type):
    '''A subscription'''
    __schema__ = mvf1_schema
    __field_names__ = ('subscription_type', 'expires_at', 'signature')
    subscription_type = sgqlc.types.Field(sgqlc.types.non_null(SubscriptionType), graphql_name='subscriptionType')
    '''The type of subscription'''

    expires_at = sgqlc.types.Field(Int, graphql_name='expiresAt')
    '''The date the subscription expires (in seconds since the epoch)'''

    signature = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='signature')
    '''A JWT token that can be used to verify the subscription  ### To
    verify:  1. Retrieve the public key from
    https://multiviewer.app/.well-known/subscription-verification-
    public-key.pub 2. Verify the signature using the public key  ###
    Example (Node.js)  ```ts import { verify } from "jsonwebtoken";
    // The public key can be retrieved from
    https://multiviewer.app/.well-known/subscription-verification-
    public-key.pub const publicKey = "---BEGIN PUBLIC KEY---\n...\n---
    END PUBLIC KEY---";  const verified = verify(token, publicKey, {
    algorithms: ["RS256"],   issuer: "multiviewer.app", }); ```
    '''



class SystemInfo(sgqlc.types.Type):
    '''Basic system information'''
    __schema__ = mvf1_schema
    __field_names__ = ('platform', 'arch')
    platform = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='platform')
    '''The current platform (win32, darwin, linux)'''

    arch = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='arch')
    '''The current CPU architecture (x64, arm64, etc.)'''




########################################################################
# Unions
########################################################################

########################################################################
# Schema Entry Points
########################################################################
mvf1_schema.query_type = Query
mvf1_schema.mutation_type = Mutation
mvf1_schema.subscription_type = Subscription

