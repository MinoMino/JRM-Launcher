JanRyuMon Launcher
by Mino - http://www.minomino.org
E-mail: mino@minomino.org

Binary builds can be found here: http://www.minomino.org/jrm
These builds do not require Python 3 to be installed on the system.

USAGE & TROUBLESHOOTING
-----------------------

You should be able to simply double-click the shortcut, type in login info, and that's it.
You might have to run this as Administrator if you are using UAC. That's probably the case
if the program exits without any errors regarding paths and such.

Note that if skip the launcher, you'll also skip JRM's updater. In other words, if JRM
suddenly stops working after using this for a while, there's likely an update out that
you need to get by using the launcher once. After that, you'll have to hope nothing changed
to the authentication process, or this program might stop working correctly.

Note that to use this, you must have the NCSoft and PlayNC software installed. To do this,
you should run JRM using IE at least once. This application will look in the following
folders for the necessary files:

%ProgramFiles%\JanRyuMon (or %HomePath%\PlayNC\JanRyuMon in some cases)
%HomePath%\AppData\LocalLow\NCLoader (Vista/7) or %HomePath%\Application Data\NCLoader (XP)
C:\PlayNC\PlayNCLauncher

If you get errors telling you that there's something that couldn't be found, you'll have
to find the files manually, and then provide the path as a command line argument. Look
at the advanced usage section.

ADVANCED USAGE
--------------

usage: jrmlauncher.py [-h] [-s] [-u USERNAME] [-p PASSWORD] [-nc NCPATH]
                      [-pnc PNCPATH] [-jrm JRMPATH]

optional arguments:
  -h, --help            show this help message and exit
  -s, --skip            If set, the PlayNC launcher is skipped altogether and
                        launches JRM directly.
  -alt, --alternative   Alternative way of launching JRM. Only works with if
                        skipping launcher.
  -u USERNAME, --username USERNAME
                        Your JRM username.
  -p PASSWORD, --password PASSWORD
                        Your JRM password.
  -nc NCPATH, --ncpath NCPATH
                        Path to the NCLoader folder.
  -pnc PNCPATH, --pncpath PNCPATH
                        Path to the PlayNC folder.
  -jrm JRMPATH, --jrmpath JRMPATH
                        Path to the JanRyuMon folder.
                        
(Note that it says "jrmlauncher.py" even in the binary build, but in that case it's "jrmlauncher.exe")

Example: jrmlauncher.exe --skip -u MyAccount -p MyPassword123 -jrm "C:\arbitrary path\plaync"

None of the arguments require another argument to be given, except for "-alt".
In other words, you are allowed to only specify your username and manually input
the password, or vice versa. The same applies to the paths. Don't forget the use
quotes if a path or password contains spaces.

The "--alternative" argument will only work with "--skip". It'll launch using a
different method. You might want to try this method if the normal method doesn't work.
The advantage of using the alternative method is that it's easier for applications to
detect the JRM process being launched if you, for instance, run it with Steam, so that
it can inject the Steam overlay into the process. (Thanks for the tip, Anon)

If you are using the binary builds, you can edit the shortcuts provided to add arguments,
or you can use batch files. You can use this to create several shortcuts with different
accounts and such. 

WHAT DOES IT DO?
----------------

By using IE, ActiveX will load a dynamic library (NCKeygen.dll) and call an exported
function that will create a key. This key is used with the POST message when you enter
your username and password over HTTPS. If it is a successful login, IE will store a
cookie with a session ID. This session ID is used by ActiveX to launch the game's
launcher with the ID as one of its command line arguments.

This program does exactly the same, but you know, without using IE and ActiveX.