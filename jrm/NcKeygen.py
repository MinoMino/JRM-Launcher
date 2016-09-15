# JRM Launcher - Launch JanRyuMon without the need of Internet Explorer and ActiveX
# Copyright (C) Mino <mino@minomino.org>

# This file is part of JRM Launcher.

# JRM Launcher is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# JRM Launcher is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with JRM Launcher. If not, see <http://www.gnu.org/licenses/>.

import os
import os.path
import ctypes

class NcKeygen():
    def __init__(self, dll_path):
        # Load DLL
        self.keygen_dll = ctypes.WinDLL(dll_path)

        # Set up prototype and parameters.
        self.keygen_proto = ctypes.WINFUNCTYPE(ctypes.c_int)
        self.keygen_params = ()

        # Map Python function to the DLL's exported function.
        self.keygen_getkey = self.keygen_proto(("GetUniqueKey", self.keygen_dll), self.keygen_params)
 
    def get_key(self):
        # Call and return unique key.
        self.keygen_result = ctypes.c_wchar_p(self.keygen_getkey())
        return self.keygen_result.value
