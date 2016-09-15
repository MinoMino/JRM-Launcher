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

import sys
from cx_Freeze import setup, Executable

executables = [Executable("jrmlauncher.py")]

build_options = { "compressed" : True,
                 "includes" : ["NcKeygen", "JrmSession"],
                 "path" : sys.path + ["jrm"]
               }

setup( name = "JanRyuMon Launcher",
       version = "0.2.3",
       description = "Launch JanRyuMon without having to use IE.",
       maintainer = "Mino",
       maintainer_email = "mino@minomino.org",
       url = "http://www.minomino.org/",
       options = dict(build_exe = build_options),
       executables = executables
     )