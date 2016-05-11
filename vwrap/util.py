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

import os
import platform
import ctypes


def load_library():
    """
    Attempts to locate and load the v-rep remote API library via a VREP
    environment variable, which is expected to describe the root installation
    directory of v-rep.
    """
    try:
        vrep_dir = os.environ['VREP']
    except KeyError:
        raise EnvVarNotSetError("VREP environment variable not set")

    lib_dir = os.path.join(
        vrep_dir, 'programming', 'remoteApiBindings', 'lib', 'lib')

    if platform.architecture()[0] == '64bit':
        lib_dir = os.path.join(lib_dir, '64Bit')
    else:
        lib_dir = os.path.join(lib_dir, '32Bit')

    if platform.system() == 'cli':
        lib_name = 'remoteApi.dll'
    elif platform.system() == 'Windows':
        lib_name = 'remoteApi.dll'
    elif platform.system() == 'Darwin':
        lib_name = 'remoteApi.dylib'
    else:
        lib_name = 'remoteApi.so'
    lib_path = os.path.join(lib_dir, lib_name)

    return ctypes.CDLL(lib_path)


class EnvVarNotSetError(RuntimeError):
    pass
