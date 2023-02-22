import sgqlc.types


mvf1_schema = sgqlc.types.Schema()



########################################################################
# Scalars and Enumerations
########################################################################
class BigInt(sgqlc.types.Scalar):
    __schema__ = mvf1_schema


Boolean = sgqlc.types.Boolean

Float = sgqlc.types.Float

ID = sgqlc.types.ID

Int = sgqlc.types.Int

class JSONObject(sgqlc.types.Scalar):
    __schema__ = mvf1_schema


class PlayerType(sgqlc.types.Enum):
    __schema__ = mvf1_schema
    __choices__ = ('ADDITIONAL', 'OBC')


String = sgqlc.types.String


########################################################################
# Input Objects
########################################################################
class PlayerCreateInput(sgqlc.types.Input):
    __schema__ = mvf1_schema
    __field_names__ = ('content_id', 'channel_id', 'driver_tla', 'driver_number', 'stream_title', 'bounds', 'fullscreen', 'always_on_top', 'maintain_aspect_ratio')
    content_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='contentId')
    channel_id = sgqlc.types.Field(Int, graphql_name='channelId')
    driver_tla = sgqlc.types.Field(String, graphql_name='driverTla')
    driver_number = sgqlc.types.Field(Int, graphql_name='driverNumber')
    stream_title = sgqlc.types.Field(String, graphql_name='streamTitle')
    bounds = sgqlc.types.Field('RectangleInput', graphql_name='bounds')
    fullscreen = sgqlc.types.Field(Boolean, graphql_name='fullscreen')
    always_on_top = sgqlc.types.Field(Boolean, graphql_name='alwaysOnTop')
    maintain_aspect_ratio = sgqlc.types.Field(Boolean, graphql_name='maintainAspectRatio')


class RectangleInput(sgqlc.types.Input):
    __schema__ = mvf1_schema
    __field_names__ = ('x', 'y', 'width', 'height')
    x = sgqlc.types.Field(Int, graphql_name='x')
    y = sgqlc.types.Field(Int, graphql_name='y')
    width = sgqlc.types.Field(Int, graphql_name='width')
    height = sgqlc.types.Field(Int, graphql_name='height')



########################################################################
# Output Objects and Interfaces
########################################################################
class LiveTimingClock(sgqlc.types.Type):
    __schema__ = mvf1_schema
    __field_names__ = ('paused', 'system_time', 'track_time', 'live_timing_start_time')
    paused = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='paused')
    system_time = sgqlc.types.Field(sgqlc.types.non_null(BigInt), graphql_name='systemTime')
    track_time = sgqlc.types.Field(sgqlc.types.non_null(BigInt), graphql_name='trackTime')
    live_timing_start_time = sgqlc.types.Field(sgqlc.types.non_null(BigInt), graphql_name='liveTimingStartTime')


class LiveTimingState(sgqlc.types.Type):
    __schema__ = mvf1_schema
    __field_names__ = ('archive_status', 'audio_streams', 'car_data', 'championship_prediction', 'content_streams', 'driver_list', 'extrapolated_clock', 'heartbeat', 'lap_count', 'lap_series', 'pit_lane_time_collection', 'position', 'race_control_messages', 'session_data', 'session_info', 'session_status', 'team_radio', 'timing_app_data', 'timing_data', 'timing_stats', 'top_three', 'track_status', 'weather_data', 'weather_data_series')
    archive_status = sgqlc.types.Field(JSONObject, graphql_name='ArchiveStatus')
    audio_streams = sgqlc.types.Field(JSONObject, graphql_name='AudioStreams')
    car_data = sgqlc.types.Field(JSONObject, graphql_name='CarData')
    championship_prediction = sgqlc.types.Field(JSONObject, graphql_name='ChampionshipPrediction')
    content_streams = sgqlc.types.Field(JSONObject, graphql_name='ContentStreams')
    driver_list = sgqlc.types.Field(JSONObject, graphql_name='DriverList')
    extrapolated_clock = sgqlc.types.Field(JSONObject, graphql_name='ExtrapolatedClock')
    heartbeat = sgqlc.types.Field(JSONObject, graphql_name='Heartbeat')
    lap_count = sgqlc.types.Field(JSONObject, graphql_name='LapCount')
    lap_series = sgqlc.types.Field(JSONObject, graphql_name='LapSeries')
    pit_lane_time_collection = sgqlc.types.Field(JSONObject, graphql_name='PitLaneTimeCollection')
    position = sgqlc.types.Field(JSONObject, graphql_name='Position')
    race_control_messages = sgqlc.types.Field(JSONObject, graphql_name='RaceControlMessages')
    session_data = sgqlc.types.Field(JSONObject, graphql_name='SessionData')
    session_info = sgqlc.types.Field(JSONObject, graphql_name='SessionInfo')
    session_status = sgqlc.types.Field(JSONObject, graphql_name='SessionStatus')
    team_radio = sgqlc.types.Field(JSONObject, graphql_name='TeamRadio')
    timing_app_data = sgqlc.types.Field(JSONObject, graphql_name='TimingAppData')
    timing_data = sgqlc.types.Field(JSONObject, graphql_name='TimingData')
    timing_stats = sgqlc.types.Field(JSONObject, graphql_name='TimingStats')
    top_three = sgqlc.types.Field(JSONObject, graphql_name='TopThree')
    track_status = sgqlc.types.Field(JSONObject, graphql_name='TrackStatus')
    weather_data = sgqlc.types.Field(JSONObject, graphql_name='WeatherData')
    weather_data_series = sgqlc.types.Field(JSONObject, graphql_name='WeatherDataSeries')


class Mutation(sgqlc.types.Type):
    __schema__ = mvf1_schema
    __field_names__ = ('version', 'player_create', 'player_delete', 'player_set_fullscreen', 'player_set_bounds', 'player_set_volume', 'player_set_paused', 'player_set_muted', 'player_seek_to', 'player_sync', 'player_set_speedometer_visibility')
    version = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='version')
    player_create = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='playerCreate', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(PlayerCreateInput), graphql_name='input', default=None)),
))
    )
    player_delete = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='playerDelete', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    player_set_fullscreen = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='playerSetFullscreen', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
        ('fullscreen', sgqlc.types.Arg(Boolean, graphql_name='fullscreen', default=None)),
))
    )
    player_set_bounds = sgqlc.types.Field(sgqlc.types.non_null('Rectangle'), graphql_name='playerSetBounds', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
        ('bounds', sgqlc.types.Arg(sgqlc.types.non_null(RectangleInput), graphql_name='bounds', default=None)),
))
    )
    player_set_volume = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='playerSetVolume', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
        ('volume', sgqlc.types.Arg(sgqlc.types.non_null(Float), graphql_name='volume', default=None)),
))
    )
    player_set_paused = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='playerSetPaused', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
        ('paused', sgqlc.types.Arg(Boolean, graphql_name='paused', default=None)),
))
    )
    player_set_muted = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='playerSetMuted', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
        ('muted', sgqlc.types.Arg(Boolean, graphql_name='muted', default=None)),
))
    )
    player_seek_to = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='playerSeekTo', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
        ('absolute', sgqlc.types.Arg(Float, graphql_name='absolute', default=None)),
        ('relative', sgqlc.types.Arg(Float, graphql_name='relative', default=None)),
))
    )
    player_sync = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='playerSync', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    player_set_speedometer_visibility = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='playerSetSpeedometerVisibility', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
        ('visible', sgqlc.types.Arg(Boolean, graphql_name='visible', default=None)),
))
    )


class Player(sgqlc.types.Type):
    __schema__ = mvf1_schema
    __field_names__ = ('id', 'type', 'state', 'driver_data', 'stream_data', 'bounds', 'fullscreen', 'always_on_top', 'maintain_aspect_ratio')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    type = sgqlc.types.Field(sgqlc.types.non_null(PlayerType), graphql_name='type')
    state = sgqlc.types.Field('PlayerState', graphql_name='state')
    driver_data = sgqlc.types.Field('PlayerDriverData', graphql_name='driverData')
    stream_data = sgqlc.types.Field('PlayerStreamData', graphql_name='streamData')
    bounds = sgqlc.types.Field(sgqlc.types.non_null('Rectangle'), graphql_name='bounds')
    fullscreen = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='fullscreen')
    always_on_top = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='alwaysOnTop')
    maintain_aspect_ratio = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='maintainAspectRatio')


class PlayerDriverData(sgqlc.types.Type):
    __schema__ = mvf1_schema
    __field_names__ = ('driver_number', 'tla', 'first_name', 'last_name', 'team_name')
    driver_number = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='driverNumber')
    tla = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='tla')
    first_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='firstName')
    last_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='lastName')
    team_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='teamName')


class PlayerState(sgqlc.types.Type):
    __schema__ = mvf1_schema
    __field_names__ = ('ts', 'paused', 'muted', 'volume', 'live', 'current_time', 'interpolated_current_time')
    ts = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='ts')
    paused = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='paused')
    muted = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='muted')
    volume = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='volume')
    live = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='live')
    current_time = sgqlc.types.Field(Float, graphql_name='currentTime')
    interpolated_current_time = sgqlc.types.Field(Float, graphql_name='interpolatedCurrentTime')


class PlayerStreamData(sgqlc.types.Type):
    __schema__ = mvf1_schema
    __field_names__ = ('content_id', 'meeting_key', 'session_key', 'channel_id', 'title')
    content_id = sgqlc.types.Field(ID, graphql_name='contentId')
    meeting_key = sgqlc.types.Field(String, graphql_name='meetingKey')
    session_key = sgqlc.types.Field(String, graphql_name='sessionKey')
    channel_id = sgqlc.types.Field(Int, graphql_name='channelId')
    title = sgqlc.types.Field(String, graphql_name='title')


class Query(sgqlc.types.Type):
    __schema__ = mvf1_schema
    __field_names__ = ('version', 'system_info', 'players', 'player', 'live_timing_state', 'live_timing_clock')
    version = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='version')
    system_info = sgqlc.types.Field(sgqlc.types.non_null('SystemInfo'), graphql_name='systemInfo')
    players = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Player))), graphql_name='players')
    player = sgqlc.types.Field(sgqlc.types.non_null(Player), graphql_name='player', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    live_timing_state = sgqlc.types.Field(LiveTimingState, graphql_name='liveTimingState')
    live_timing_clock = sgqlc.types.Field(LiveTimingClock, graphql_name='liveTimingClock')


class Rectangle(sgqlc.types.Type):
    __schema__ = mvf1_schema
    __field_names__ = ('x', 'y', 'width', 'height')
    x = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='x')
    y = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='y')
    width = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='width')
    height = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='height')


class SystemInfo(sgqlc.types.Type):
    __schema__ = mvf1_schema
    __field_names__ = ('platform', 'arch')
    platform = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='platform')
    arch = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='arch')



########################################################################
# Unions
########################################################################

########################################################################
# Schema Entry Points
########################################################################
mvf1_schema.query_type = Query
mvf1_schema.mutation_type = Mutation
mvf1_schema.subscription_type = None

