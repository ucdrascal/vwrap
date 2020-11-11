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

# path to root of v-rep installation
vrep_path = os.environ.get('VREP')

# mapping from platform name to remote API lib extension
libext_map = {
    'Windows': '.dll',
    'Mac': '.dylib',
    'Linux': '.so'
}

# mapping from `platform.system()` to v-rep platform name
# pulled from v-rep's supplied mapping
platform_map = {
    'cli': 'Linux',
    'Windows': 'Windows',
    'Darwin': 'Mac'
}

libpath_fmt = os.path.join('{vrep_path}', 'programming', 'remoteApiBindings',
                           'lib', 'lib', '{platform}', 


def load_library():
    """Attempt to locate and load the v-rep remote API library.

    The ``VREP`` environment variable should be set so that the library can be
    found. It should be set to the root directory of the v-rep installation.
    """
    if vrep_path is None:
        raise PathNotSetError("VREP path not set")

    lib_path = os.path.join(vrep_path, 'programming', 'remoteApiBindings',
                            'lib', 'lib')

    if platform.architecture()[0] == '64bit':
        arch = '64Bit'
    else:
        arch = '32Bit'


    libpath = os.path.join(vrep_path, 'programming', 'remoteApiBindings',
            'lib', 'lib', platform

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


class PathNotSetError(RuntimeError):
    pass
