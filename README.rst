***************
mvf1
***************

A Python package and command line interface to control video players for
`MultiViewer For F1`_, the best way to watch Formula 1.

.. image:: https://dl.circleci.com/status-badge/img/gh/RobSpectre/mvf1/tree/main.svg?style=svg
        :target: https://dl.circleci.com/status-badge/redirect/gh/RobSpectre/mvf1/tree/main

.. image:: https://codecov.io/gh/RobSpectre/mvf1/branch/main/graph/badge.svg?token=L5N96KXN2V 
 :target: https://codecov.io/gh/RobSpectre/mvf1

.. image:: https://readthedocs.org/projects/mvf1/badge/?version=latest
    :target: https://mvf1.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status


Table of Contents
=================


.. contents::
    :local:
    :depth: 1
    :backlinks: none


Features
===============

* Command line interface for controlling `MultiViewer For F1`_. Useful for
  integrations with control interfaces like `StreamDeck`_
* Pythonic interface for controlling `MultiViewer For F1`_. No GraphQL needed!
* `Type hints`_
* `Full documentation`_
* `Test coverage`_
* `black`_ Praise the Dark Lord


Installation
===============

The latest version can be installed via `pip`_.

.. code-block:: bash

   $ pip install mvf1


Quickstart
================

Command Line
----------------

.. code-block:: bash

    $ mvf1-cli --help

Library
----------------

Displaying all players

.. code-block:: python

    >>> from mvf1 import MultiViewerForF1
    >>> remote = MultiViewerForF1()
    >>> remote.players
    [6: INTERNATIONAL, 7: PER]

Pause all players

.. code-block:: python

    >>> from mvf1 import MultiViewerForF1
    >>> remote = MultiViewerForF1()
    >>> for player in remote.players:
    >>>     player.mute()
    {'data': {'playerSetMuted': True}}
    {'data': {'playerSetMuted': True}}

Retrieve specific player

.. code-block:: python

    >>> from mvf1 import MultiViewerForF1
    >>> remote = MultiViewerForF1()
    >>> player = remote.player(6)
    >>> player.state
    {'ts': 1677168293.21, 'paused': False, 'muted': True, 'volume': 100, 'live': False, 'currentTime': 10.002025, 'interpolatedCurrentTime': 363.656025}

Switch stream of player to data channel

.. code-block:: python

    >>> from mvf1 import MultiViewerForF1
    >>> remote = MultiViewerForF1()
    >>> player = remote.player(6)
    >>> player.switch_stream('DATA')
    {'data': {'playerCreate': '12'}}

Synchronize all players to specific player

.. code-block:: python

    >>> from mvf1 import MultiViewerForF1
    >>> remote = MultiViewerForF1()
    >>> player = remote.player(6)
    >>> player.sync()
    {'data': {'playerSync': True}}

Synchornize all players to player streaming broadcast commentary

.. code-block:: python

    >>> from mvf1 import MultiViewerForF1
    >>> remote = MultiViewerForF1()
    >>> remote.player_sync_to_commentary()
    {'data': {'playerSync': True}}


Development
================

Hacking
---------------

To hack on the project, clone the `GitHub repo`_:

.. code-block:: bash
   
   $ git clone https://github.com/RobSpectre/mvf1

Then install in a `virtualenv`_.

.. code-block:: bash

   $ pip install -e ./


Test
---------------

The project uses `tox`_ for tests. Simply run from project root

.. code-block:: bash

    $ tox


Meta
================

* Written by `Rob Spectre`_.
* Released under `MIT License`_.
* Software is as is - no warranty expressed or implied, diggity.
* This package is not developed or maintained by `MultiViewer For F1`_ or
  `Formula 1 TV`.
* Shout out to the excellent `MultiViewer For F1`_ team! This app absolutely
  changed how I enjoy Formula 1.
* 🏎️ ¡Vamos Checo! 🏎️


.. _MultiViewer for F1: https://multiviewer.app/
.. _pip: https://multiviewer.app/
.. _GitHub Repo: https://github.com/RobSpectre/mvf1
.. _virtualenv: https://multiviewer.app/
.. _Rob Spectre: https://brooklynhacker.com
.. _MIT License: http://opensource.org/licenses/MIT
.. _tox: https://tox.wiki/en/latest/
.. _black: https://black.readthedocs.io/en/stable/
.. _StreamDeck: https://www.elgato.com/en/welcome-to-stream-deck
.. _type hints: https://docs.python.org/3/library/typing.html
.. _Full documentation: https://mvf1.readthedocs.io/en/latest/
.. _Test coverage: https://app.codecov.io/gh/RobSpectre/mvf1
