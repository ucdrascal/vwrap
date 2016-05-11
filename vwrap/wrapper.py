# Copyright (C) 2016 Kenneth Lyons <ixjlyons@gmail.com>
#
# This file is part of vwrap.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from vwrap import vrep


CTRL_ENABLED_PARAM = 2001


class VrepSimulation(object):
    """
    A simple client to vrep's remote API server.

    Parameters
    ----------
    host : str, optional
        IP address of the vrep remote server. By default, localhost
        ('127.0.0.1') is used, which indicates the serveris running on the
        user's machine.
    port : int, optional
        Port that the vrep server is running on. By default, 19997 is used,
        which is the default port the remove server runs on.

    Attributes
    ----------
    client_id : int
        This program's ID given to us by the remote API server.
    """

    def __init__(self, host='127.0.0.1', port=19997):
        self.host = host
        self.port = port

        self._connected = False
        self._running = False

        self._connect()

    def __enter__(self):
        if not self._connected:
            self._connect()

        if not self._running:
            self.start()

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self._running:
            self.stop()

        if self._connected:
            self._disconnect()

    def start(self):
        """
        Starts the simulation. Use stop() to stop the simulation or finish() to
        stop and kill the connection to the v-rep server.
        """
        ret = vrep.simxStartSimulation(
            self.client_id,
            vrep.simx_opmode_oneshot_wait)
        _validate(ret)
        self._running = True

    def stop(self):
        """
        Stops the simulation. Can be started again.
        """
        ret = vrep.simxStopSimulation(
            self.client_id,
            vrep.simx_opmode_oneshot_wait)
        _validate(ret)
        self._running = False

    def finish(self):
        """
        Stops the simulation and disconnects from v-rep. Starting the
        simulation after this won't work. Create a new instance to reconnect.
        """
        self.stop()
        self._disconnect()
        self._connected = False

    def _connect(self):
        vrep.simxFinish(-1)
        cid = vrep.simxStart(self.host, self.port, True, True, 1000, 5)
        if cid == -1:
            raise Exception('Failed to connect V-REP remote API server.')

        self.client_id = cid
        self._connected = True

    def _disconnect(self):
        vrep.simxFinish(self.client_id)
        self._connected = False


class Scene(object):
    """
    Handles to items in the v-rep scene.
    """

    def __init__(self, client_id):
        self.client_id = client_id

        self._initialize_joints()

    def _initialize_joints(self):
        err, handles, _, _, names = vrep.simxGetObjectGroupData(
            self.client_id, vrep.sim_object_joint_type, 0,
            vrep.simx_opmode_oneshot_wait)

        self.joint_handles = dict(zip(names, handles))
        self._joint_objects = {}

    def get_joint(self, name):
        try:
            joint = self._joint_objects[name]
        except KeyError:
            joint = Joint(self.client_id, name, self.joint_handles[name])

        return joint


class Joint(object):

    def __init__(self, client_id, name, handle):
        self.client_id = client_id
        self.name = name
        self.handle = handle
        self.velocity = 0
        self.position = 0

        self._init_control_mode()

        self.initial_position = self._get_position(
            opmode=vrep.simx_opmode_oneshot_wait)

        # set up streaming position input
        self._get_position(opmode=vrep.simx_opmode_streaming)

    def update(self, opmode=None):
        if opmode is None:
            opmode = vrep.simx_opmode_oneshot

        if self.position_controlled:
            res = vrep.simxSetJointTargetPosition(
                self.client_id, self.handle, self.position, opmode)
        else:
            res = vrep.simxSetJointTargetVelocity(
                self.client_id, self.handle, self.velocity, opmode)

        if opmode == vrep.simx_opmode_oneshot_wait:
            _validate(res)

        if not self.position_controlled:
            self.position = self._get_position(
                opmode=vrep.simx_opmode_buffer)

    def set_position_controlled(self, position_controlled):
        """
        Sets the joint mode. Either position controlled or velocity controlled
        """
        self.position_controlled = position_controlled
        mode = 1 if position_controlled else 0
        vrep.simxSetObjectIntParameter(
            self.client_id, self.handle, CTRL_ENABLED_PARAM,
            mode, vrep.simx_opmode_oneshot)

    def _init_control_mode(self):
        err, ctrl = vrep.simxGetObjectIntParameter(
            self.client_id, self.handle, CTRL_ENABLED_PARAM,
            vrep.simx_opmode_oneshot_wait)
        self.position_controlled = not (ctrl == 0)

    def _get_position(self, opmode=None):
        if opmode is None:
            opmode = vrep.simx_opmode_oneshot

        res, pos = vrep.simxGetJointPosition(
            self.client_id, self.handle, opmode)

        if opmode == vrep.simx_opmode_oneshot_wait:
            _validate(res)

        return pos


class Signal(object):
    """
    Simple interface to signals in v-rep child scripts.

    Parameters
    ----------
    client_id : int
        The v-rep simulation client ID (obtained from `VrepSimulation`)
    name : str
        The name of the signal, as it is named in the v-rep scene.
    functions: dict
        Dictionary of remote API functions for handling the signal. Required
        keys are 'set', 'get', and 'clear'.
    """

    def __init__(self, client_id, name, functions):
        self.client_id = client_id
        self.name = name
        self.functions = functions

        self._first_read = True

    def read(self):
        """
        Reads the signal.

        Returns
        -------
        sig : relevant type for the signal (str, float, or int)
            The signal value if it has been set on the v-rep side. Returns None
            if it has not been set.
        """
        if self._first_read:
            opmode = vrep.simx_opmode_streaming
            self._first_read = False
        else:
            opmode = vrep.simx_opmode_buffer

        err, sig = self.functions['get'](
            self.client_id,
            self.name,
            opmode)

        if err == vrep.simx_return_ok:
            self._clear()
        else:
            sig = None

        return sig

    def write(self, value):
        """
        Writes a value to the signal.

        Parameters
        ----------
        value : relevant type for the signal (str, float, or int)
            Value to send to the signal.
        """
        self.functions['set'](
            self.client_id,
            self.name,
            value,
            vrep.simx_opmode_oneshot)

    def _clear(self):
        self.functions['clear'](
            self.client_id,
            self.name,
            vrep.simx_opmode_oneshot)


class StringSignal(Signal):
    """
    Class for convenient interfacing with string signals in v-rep.

    Parameters
    ----------
    client_id : int
        The v-rep simulation client ID (obtained from `VrepSimulation`)
    name : str
        The name of the signal, as it is named in the v-rep scene.
    """

    functions = {
        'set': vrep.simxSetStringSignal,
        'get': vrep.simxGetStringSignal,
        'clear': vrep.simxClearStringSignal
    }


class FloatSignal(Signal):
    """
    Class for convenient interfacing with float signals in v-rep.

    Parameters
    ----------
    client_id : int
        The v-rep simulation client ID (obtained from `VrepSimulation`)
    name : str
        The name of the signal, as it is named in the v-rep scene.
    """

    functions = {
        'set': vrep.simxSetFloatSignal,
        'get': vrep.simxGetFloatSignal,
        'clear': vrep.simxClearFloatSignal
    }


class IntegerSignal(Signal):
    """
    Class for convenient interfacing with integer signals in v-rep.

    Parameters
    ----------
    client_id : int
        The v-rep simulation client ID (obtained from `VrepSimulation`)
    name : str
        The name of the signal, as it is named in the v-rep scene.
    """
    functions = {
        'set': vrep.simxSetIntegerSignal,
        'get': vrep.simxGetIntegerSignal,
        'clear': vrep.simxClearIntegerSignal
    }


def _check_suffix(name, suffix):
    if suffix == '':
        if len(name.split('#')) == 1:
            return True
        else:
            return False
    else:
        if suffix in name:
            return True
        else:
            return False


def _validate(res):
    if res != vrep.simx_return_ok:
        err = ""
        if res == vrep.simx_return_novalue_flag:
            err = "Input buffer doesn't contain the specified command"
        elif res == vrep.simx_return_timeout_flag:
            err = "Command reply not received in time for wait opmode"
        elif res == vrep.simx_return_illegal_opmode_flag:
            err = "Command odesn't support specified opmode"
        elif res == vrep.simx_return_remote_error_flag:
            err = "Command caused an error on the server side"
        elif res == vrep.simx_return_split_progress_flag:
            err = "Previous similar command not processed yet"
        elif res == vrep.simx_return_local_error_flag:
            err = "Command caused an error on the client side"
        elif res == vrep.simx_return_initialize_error_flag:
            err = "simxStart not yet called"
        else:
            err = "Unknown v-rep error code: %s" % hex(res)

        raise ValueError(err)
