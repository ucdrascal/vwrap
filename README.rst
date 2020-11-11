=====
vwrap
=====

High-level wrapper for controlling `V-REP`_ simulations with Python.

This library has three main purposes. First, it packages V-REP's Python
bindings for their remote API, making it a bit more convenient to start using
the remote API from Python. Specifically, you can install ``vwrap`` and then
start using the remote API without copying files or ensuring your scripts are
in the correct directory.


Installation
============

You can install ``vwrap`` via ``pip``::

    $ pip install vwrap

After installation, you need to tell ``vwrap`` where V-REP is installed on your
system.

Getting Started
===============

In order to work, ``vwrap`` needs to know the path to your V-REP installation.
On Windows, this is something like ``C:\Program Files\V-REP3\V-REP_PRO_EDU``.
On Linux, it is wherever you decompressed the tarball. You can then set the
path in your script like this:

.. code-block:: python

   import vwrap
   vwrap.set_path('~/vrep/vrep-3.5.0')

   sim = vrep.VrepSimulation()
   sim.start()
   sim.finish()

As an alternative, if you don't want to hard-code the V-REP installation path
in your scrips, you can set the ``VREP`` environment variable to the path and
``vwrap`` will use it.

Other Notes
===========

This repository likely won't be updated as frequently as V-REP releases are
made, so you may run into issues with that. According to Coppelia, `the remote
API is fairly stable
<https://github.com/CoppeliaRobotics/v_repExtRemoteApi/pull/1#issuecomment-346622793>`
so this shouldn't really happen much. If a remote API function has recently
been added and you need to use it, you can open an issue and/or add it yourself
by merging the ``vrep.py`` and ``vrepConst.py`` files from the
`v_repExtRemoteApi`_ repository with the ones here. Note that a few minor
modifications were made to the files contained here, so the merge process
should be done carefully.

.. _V-REP: http://www.coppeliarobotics.com/
.. _remote API: http://www.coppeliarobotics.com/helpFiles/en/remoteApiOverview.htm
.. _v_repExtRemoteApi: https://github.com/CoppeliaRobotics/v_repExtRemoteApi
