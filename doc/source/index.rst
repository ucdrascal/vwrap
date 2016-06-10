vwrap
=====

vwrap is intended to be a pythonic wrapper around the Python bindings
to the remote API provided by Coppelia Robotics for controlling the Virtual
Robot Experimentation Platform (V-REP).


Why a Wrapper?
--------------

Understandably, the Python bindings to the V-REP remote API are simply a thin
wrapper around the underlying C implementation. This results in a huge
collection of functions (with long names) for controlling and manipulating the
V-REP scene. It is much nicer to work with objects which represent the
simulation, the scene, the robots in the scene, the joints in the robots, etc.
vwrap takes care of memorizing the function and constant names, providing
a high-level interface to the simulation. While this makes things convenient,
the convenience inherently comes at the cost of limited flexibility with
respect to the full implementation provided by V-REP.


.. toctree::
    :maxdepth: 1
    :glob:
    :hidden:

    installation
    usage
    api
