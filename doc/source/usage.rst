Getting Started
===============

vwrap is made to be pretty simple to get running. The basic functionality is
covered here.

VrepSimulation
--------------

The :class:`vwrap.wrapper.VrepSimulation` class implements the basic connection
to the V-REP remote API server. The client (i.e. the program you're writing)
can be run on the same machine as the one running V-REP (default) or it can be
connected remotely by specifying the IP address of the machine running V-REP.
By default, the remote API server runs on port ``19997``. This can be changed
by editing the ``remoteApiConnections.txt`` file in the V-REP installation
directory.

With a :class:`vwrap.wrapper.VrepSimulation` connection, the simulation can be
started and stopped.
