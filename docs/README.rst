shellcuts - directory shortcuts for your shell
----------------------------------------------

Shellcuts are directory shortcuts for your shell. This program allows you to save locations as 'shellcuts' and then cut back to those locations with a single, short command. This program is inspired by Bashmarks and hopes to improve on Bashmarks_ by supporting more systems and shells. Shellcuts includes the following features:

- creates named shellcuts to any location in the filesystem
- lists all saved shellcuts
- deletes shellcuts by name
- saves shellcuts on a per-user basis
- supports Bashmarks syntax for user comfort and familiarity

Planned features include:

- tab completion
- Fish, Zsh, Csh, Korn shell support
- installable via APT, Homebrew
- z-like_ features

installation
------------

Shellcuts is meant to be easy to install--use any of the following methods. You need the latest version of `Python 3`_ installed for it to work!

**METHOD 1:** Install with wget and dpkg
If you use a Debian-based machine (Ubuntu, Linux Mint, Debian, etc) then this method will work until APT support is added. Run the following command:
::
  $ dunno yet will add soon

**METHOD 2:** Install with APT_ (PLANNED)

If you are running a Linux distribution that uses Apt to manage packages (e.g. Ubuntu, Kubuntu, Debian), run this command to install Shellcuts:
::
  $ sudo apt install shellcuts

**METHOD 3:** Install with Homebrew_ (PLANNED)

If you're on Mac and have Homebrew installed, run this command to install Shellcuts:
::
  $ brew install shellcuts

**METHOD 4:** Manually Install with Git_ (PLANNED)

If, for whatever reason, the other methods don't work for you or maybe just aren't your cup of tea, you can clone this repository and use the supplied installation script to manually install the package. This isn't recommended, however, because this method will not automatically keep Shellcuts up-to-date with the latest features. To install this way, run these commands:
::
  $ git clone https://www.github.com/tgsachse/shellcuts.git
  $ ./shellcuts/install_shellcuts.sh

usage
-----
The configuration utility that runs during installation can automatically configure your system, or if you'd prefer it can show you how to do the configuration manually. It's highly recommended that you use the automatic configuration, as it's safe from human error and is really easy! If you want to re-run the configuration utility, use this command:
::
  $ sc --init

The core command for Shellcuts is ``sc`` and by default this program includes the aliases:

- ``shellcut``
- ``shellcuts``
- ``shellc``
- ``scut``

Feel free to use any of the above or the main ``sc`` command to operate Shellcuts. This program also includes aliases to replicate Bashmarks_ syntax. They are as follows:

- ``s`` to save, equivalent to ``sc -n``
- ``g`` to go, equivalent to ``sc``
- ``p`` to print, equivalent to ``sc -p``
- ``d`` to delete, equivalent to ``sc -d``
- ``l`` to list, equivalent to ``sc -l``

Here is a list of all available options/flags:

DELETE: ``-d, --delete [shellcut]``
  Delete the specified shellcut if it exists.
(planned) HELP: ``-h, --help``
  Display a help menu for quick reference.
LIST: ``-l, --list``
  List all available shellcuts.
NEW: ``-n, --new [shellcut]``
  Create a new shellcut for the current working directory.
PRINT: ``-p, --print [shellcut]``
  Print the specified shellcut to the screen.
(planned) VERSION: ``-v, --version``
  Display version information.
(planned) BASHMARKS SYNTAX: ``--enable-bashmarks-syntax, --disable-bashmarks-syntax``
  Enable or disable Bashmarks syntax. (default: enabled)
(planned) Z SETTINGS: ``--enable-z, --disable-z``
  Enable or disable z-like features. (default: enabled)
(planned) REINITIALIZE: ``--init``
  Launch the initialization script.
  
examples
--------
Here are some examples of Shellcuts in action. See this program's man page for more.
::
  $ pwd                               # Show current directory
  /home/tgsachse/Downloads
  
  $ sc -n dloads                      # Save current directory as shellcut named 'dloads'
  $ cd /bin                           # Change directory to /bin
  $ pwd                               # Show current directory
  /bin
  
  $ sc -n bin                         # Save current directory as shellcut named 'bin'
  $ sc dloads                         # Move to location saved as shellcut 'bin'
  $ pwd                               # Show current directory
  /home/tgsachse/Downloads

  $ sc -l                             # List all saved shellcuts
  SHELLCUTS
  dloads : /home/tgsachse/Downloads
  bin : /bin

  $ sc -d dloads                      # Delete shellcut 'dloads'
  $ sc -l                             # List all saved shellcuts
  SHELLCUTS
  bin : /bin
  
  $ sc -p bin                         # Print a specific shellcut 'bin'
  bin : /bin

.. _Bashmarks: https://www.github.com/huyng/bashmarks
.. _z-like: https://github.com/rupa/z
.. _`Python 3`: https://www.python.org
.. _Pip: https://pip.pypa.io/en/stable/
.. _APT: https://en.wikipedia.org/wiki/APT_(Debian)
.. _Homebrew: https://brew.sh/
.. _Git: https://git-scm.com
