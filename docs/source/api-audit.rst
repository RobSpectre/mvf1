Dependency and GraphQL audit
============================

Checked on 2026-11-07 against PyPI and the local MultiViewer 2.15.2
GraphQL endpoint. The endpoint's introspection result is the source of
truth for the schema changes below; the public
`MultiViewer changelog <https://multiviewer.app/changelog>`_ provides context
but is not a complete API specification.

Dependencies
------------

The latest stable runtime releases checked were Click 8.5.1, FastMCP 4.1.6,
sgqlc 18, and requests 2.34.2. Updated Click and FastMCP minimum versions in
both dependency manifests; sgqlc and requests were already current.
Python 3.10 remains the minimum supported version. Build requirements now
use setuptools 84.2.1 and wheel 0.48.0, with SPDX license metadata.

Validation of the dependency/schema refresh: all 95 tests passed on Python
3.10 and 3.12 with the latest runtime dependencies; Python 3.12 coverage
was 98%. Source distribution
and wheel builds succeeded. Generated version, system information, player
list, F1 timing, and WEC timing queries validated against the captured
2.15.2 schema. The full tox interpreter matrix was not run.

GraphQL changes
---------------

* **Breaking WEC response change:** ``FIAWECLiveTimingState`` now contains
  ``positions``, ``session``, and ``raceControl``. The previous fields
  ``entries``, ``referential``, ``params``, ``flags``, ``best_sectors``,
  ``race_control``, ``laps``, and ``stints`` are gone. Regenerating the schema
  fixes the selection sent by the Python property and MCP tool. Consumers
  must use the new response keys. The regenerated WEC query targets the new
  API and will not work against older apps exposing only the old fields.
* ``SubscriptionType`` adds ``F1TV_PREMIUM``.
* ``streamOverlayReportHeights(slotId: String!, heights: JSONObject!)`` is
  a new mutation for reporting banner row heights.
* ``SubscriptionRoot.streamOverlaySlot(slotId: String!)`` is a new
  subscription, available only over WebSocket at ``/api/graphql``. Its
  ``StreamOverlaySlot`` result contains alignment, anchor, dimensions,
  current banners, and upcoming banners. The generated schema now uses the
  correct subscription root.
* Player volume documentation now permits 200% for F1 TV v2 players with
  "Allow volume above 100%" enabled. Existing setters already forward these
  values without clamping.
* Root query fields and existing player mutation signatures are unchanged.
  ``liveTimingState`` and ``liveTimingClock`` remain deprecated; the Python
  aliases already use their ``f1LiveTiming*`` replacements.

Python and MCP coverage
-----------------------

The previously missing convenience interfaces are now exposed:

* Python ``remote.active_subscriptions`` and MCP ``active_subscriptions()``
  return the GraphQL response with ``data.activeSubscriptions``. Each entry
  contains ``subscriptionType``, ``expiresAt`` (epoch seconds, or null), and
  ``signature`` (the subscription verification JWT).
* ``player_create(..., channel_id=...)`` accepts a channel ID in Python and
  MCP, as an alternative to selecting a feed by driver or stream title.
  The optional parameter is appended to preserve existing positional calls.
* ``player_set_always_on_top(..., level=...)`` and
  ``Player.set_always_on_top(..., level=...)`` accept the window-level enum
  names. The MCP tool accepts the same argument. Omitted levels retain the
  server default; invalid names raise an error before making an API call.
* Seek and volume methods accept fractional values throughout the Python
  and MCP interfaces. Negative relative seeks and integer inputs still work.

After adding these interfaces, 112 tests and 14 subtests passed on Python
3.10 and 3.12, with 98% coverage on Python 3.12. The five new or updated
operations also validated against the captured MultiViewer 2.15.2 schema.
Control operations were tested with mocks; no live players were changed.

Stream-overlay height reporting and slot subscriptions remain intentionally
unwrapped. Subscriptions require a WebSocket transport; the library currently
uses HTTP only.

Refreshing the schema
---------------------

With MultiViewer running, use the installed sgqlc tools from the project
environment. Introspection only reads schema metadata; it does not change
players. Keep descriptions and deprecated fields when generating:

.. code-block:: bash

   python -m sgqlc.introspection --timeout 10 \
       http://localhost:10101/api/graphql /tmp/mvf1-schema.json
   python -m sgqlc.codegen schema --docstrings \
       /tmp/mvf1-schema.json mvf1/mvf1_schema.py
   pytest --cov=./

Review the generated diff before accepting it. Never hand-edit
``mvf1/mvf1_schema.py``. Automated tests mock HTTP and do not need a running
MultiViewer instance.
