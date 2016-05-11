=====
vwrap
=====

High-level wrapper for controlling `V-REP`_ simulations with Python.


Locating the Remote API Library
-------------------------------

The (slightly modified) Python bindings to the `remote API`_ packaged
with V-REP itself are included here to simplify usage. The modifications make
it somewhat easier to load the remote API library. Instead of looking for the
binary in the current directory, the library looks for a ``VREP``  environment
variable, which should be set to the root directory of the v-rep install.


.. _V-REP: http://www.coppeliarobotics.com/
.. _remote API: http://www.coppeliarobotics.com/helpFiles/en/remoteApiOverview.htm
