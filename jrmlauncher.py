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
import sys
import argparse
import subprocess
import jrm

VERSION = "0.2.3"

# Initializes and returns the command-line argument parser object.
def init_parser():
    parser = argparse.ArgumentParser(description= \
             "Launch JRM without having to use IE and ActiveX. Read the README for detailed information.")
    parser.add_argument("-s", "--skip", action="store_true", \
                        help="If set, the PlayNC launcher is skipped altogether and launches JRM directly.")
    parser.add_argument("-alt", "--alternative", action="store_true", \
                        help="Alternative way of launching JRM. Only works with if skipping launcher.")
    parser.add_argument("-u", "--username", help="Your JRM username.")
    parser.add_argument("-p", "--password", help="Your JRM password.")
    parser.add_argument("-nc", "--ncpath", help="Path to the NCLoader folder.")
    parser.add_argument("-pnc", "--pncpath", help="Path to the PlayNC folder.")
    parser.add_argument("-jrm", "--jrmpath", help="Path to the JanRyuMon folder.")
    
    return parser

# Set paths needed if searching for any of the folders automatically.
def get_environ():
    program_files = os.environ["ProgramFiles"] # Should point to the x86 folder on both 32-bit and 64-bit.
    user_profile = os.path.join(os.environ['HomeDrive'], os.environ['HomePath'])
    
    return (program_files, user_profile)

# Attempts to find all the necessary files and folders and returns them.
def get_paths(args):
    
    program_files, user_profile = get_environ()
    keygen_path = ""
    launcher_path = ""
    jrm_folder_path = ""
    
    # NCLoader
    if not args.ncpath:
        w7_appdata = user_profile + "\\AppData\\LocalLow\\"
        xp_appdata = user_profile + "\\Application Data\\"
        if os.path.exists(w7_appdata + "NCLoader\\NCKeygen.dll"):
            nc_folder = w7_appdata + "NCLoader"
        elif os.path.exists(xp_appdata + "NCLoader\\NCKeygen.dll"):
            nc_folder = xp_appdata + "NCLoader"
        else:
            print("ERROR: Could not locate the NCSoft key generator automatically.")
            input()
            exit(1)
        keygen_path = nc_folder + "\\NCKeygen.dll"
    else:
        keygen_path = args.ncpath + "\\NCKeygen.dll"
    
    if not args.skip:
        # PlayNC. Only if not skipped.
        if not args.pncpath:
            pncl_folder = "C:\\PlayNC\\PlayNCLauncher"
            if not os.path.exists(pncl_folder + "\\playnclauncher.exe"):
                print("ERROR: Could not locate the PlayNC launcher automatically.")
                input()
                exit(1)
            launcher_path = pncl_folder + "\\playnclauncher.exe"
        else:
            launcher_path = args.pncpath + "\\PlayNCLauncher\\playnclauncher.exe"
    
    if args.skip:
        # JRM. Only if skipped.
        if not args.jrmpath:
            if os.path.exists("{0}\\JanRyuMon\\JanRyuMon.exe".format(program_files)):
                jrm_folder = "{0}\\JanRyuMon".format(program_files)
            elif os.path.exists("{0}\\PlayNC\\JanRyuMon\\JanRyuMon.exe".format(user_profile)):
                jrm_folder = "{0}\\PlayNC\\JanRyuMon".format(user_profile)
            else:
                print("ERROR: Could not locate JanRyuMon automatically.")
                input()
                exit(1)
            jrm_folder_path = jrm_folder
        else:
            jrm_folder_path = args.jrmpath
    
    return (keygen_path, launcher_path, jrm_folder_path)

# Prompt username and password if necessary, then return them.
def get_login(args):
    if not args.username:
        username = input("Username: ")
    else:
        username = args.username
    if not args.password:
        password = input("Password: ")
    else:
        password = args.password
        
    return (username, password)

# Initialize keygen and get unique ID.
def get_ukey(keygen_path):
    keygen = jrm.NcKeygen(keygen_path)
    ukey = keygen.get_key()
    if not ukey:
        print("ERROR: Failed to get a unique key.")
        input()
        exit(1)
        
    return ukey
    
# Initialize session object and get session ID.
def get_session_id(username, password, ukey):
    session = jrm.JrmSession(ukey)
    if not session.login(username, password):
        print("ERROR: Failed to get a session ID. Incorrect username/password?")
        input()
        exit(1)
        
    return session.session_id


        
def launch_jrm(jrm_folder_path, session_id, alternative=False):
    # Launch JRM directly.
    jrm_params = ('{0}\\JanRyuMon.exe'.format(jrm_folder_path),
                  '/SessKey:"{0}"'.format(session_id),
                  '/ChannelGroupIndex:"-1"',
                  '/ServerAddr:"106.186.45.130"',
                  '/StartGameID:"JanRyuMon"',
                  '/RepositorySub:"localhost"',
                  '/GamePath:"{0}"'.format(jrm_folder_path))
    
    if alternative:
        return os.execv('{0}\\JanRyuMon.exe'.format(jrm_folder_path), jrm_params)
    else:
        return subprocess.Popen(" ".join(jrm_params), shell=False)
    
def launch_launcher(launcher_path, session_id):
    # Launch the launcher.
    launcher_params = (launcher_path,
                       '/GameID:"PlayNCLauncher"',
                       '/ServiceFolder:"PlayNC"',
                       '/SetupMng:"NCSetupMng"',
                       '/LUpdateAddr:"uis.plaync.jp/UniUpdTool"',
                       '/FileUpdateAddr:"http://uniupdate.plaync.jp/UniUpdTool/system"',
                       '/StartGameID:"JanRyuMon"',
                       '/SessKey:"{0}"'.format(session_id))
    
    return subprocess.Popen(" ".join(launcher_params), shell=False)

if __name__ == "__main__":
    print("JanRyuMon Launcher v{0}".format(VERSION))
    print("by Mino - http://www.minomino.org\n")
    
    # Initialize command-line argument parser and parse if anything to parse.
    parser = init_parser()
    if len(sys.argv) > 1:
        args = parser.parse_args(sys.argv[1:])
    else:
        args = parser.parse_args([])
    
    # Get necessary paths.
    if not args.ncpath and not args.pncpath and not args.jrmpath:
        print("Trying to find paths automatically...")
    elif args.ncpath and args.pncpath and args.jrmpath:
        print("Using specified paths...")
    else:
        print("Using specified path(s). Trying to find the remaining...")
    keygen_path, launcher_path, jrm_folder_path = get_paths(args)
    
    # Get login info.
    if args.username and args.password:
        print("Using provided username and password.")
    username, password = get_login(args)
    
    # Get unique key
    print("Generating unique key...")
    ukey = get_ukey(keygen_path)
    
    # Get session ID
    print("Logging in as '{0}'...".format(username))
    session_id = get_session_id(username, password, ukey)
    
    # Launch either launcher or JRM.
    if not args.skip:
        print("Starting the PlayNC launcher...")
        launch_launcher(launcher_path, session_id)
    else:
        print("Skipping the PlayNC launcher. Starting JanRyuMon...")
        if args.alternative:
            print("Launching with the alternative method...")
            launch_jrm(jrm_folder_path, session_id, args.alternative)
        else:
            launch_jrm(jrm_folder_path, session_id)
    
    
    print("\nGood luck, fellow lesbian.")
    input("Press enter to close this window.")




    