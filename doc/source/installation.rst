Installation
============

vwrap is implemented in pure Python, so installation of the library itself is
pretty simple. However, the setup process involves an extra step in setting
a ``VREP`` environment variable.


Installing From Source
----------------------

vwrap uses setuptools, so installation from source is straightforward::

    python setup.py install


Setting Up
----------

vwrap relies directly on V-REP's remote API bindings, which in turn rely
directly on loading a compiled C library (loaded via `ctypes
<https://docs.python.org/3.5/library/ctypes.html>`_). To find this file in the
V-REP installation file structure, vwrap needs to be told where V-REP is
installed. This is done through an environment variable: ``VREP``.

Linux
~~~~~

On Linux systems, you can set an environment variable permanently by add the
following to your local ``.bashrc`` file::

    VREP=/path/to/vrep

If you're using a different login shell, it is expected that you can figure out
how to do this for your system.
