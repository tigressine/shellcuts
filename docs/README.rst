shellcuts - directory shortcuts for your shell
----------------------------------------------

Shellcuts are directory shortcuts for your shell. This program allows you to save locations as 'shellcuts' and then cut back to those locations with a single, short command. This program is inspired by Bashmarks and hopes to improve on Bashmarks_ by supporting more systems and shells. Shellcuts includes the following features:

- creates named shellcuts to any location in the filesystem
- lists all saved shellcuts
- deletes shellcuts by name
- saves shellcuts on a per-user basis
- Bashmarks syntax can be enabled for user comfort and familiarity
- supports Bash, Fish, and Zsh

Planned features include:

- tab completion
- Csh, Korn shell support
- installable via APT, DNF, Homebrew
- z-like_ features
- local, non-administrator installs

installation
------------

Shellcuts is meant to be easy to install--use any of the following methods. You need the latest version of `Python 3`_ installed for it to work!

**METHOD 1:** Install with wget and dpkg   
If you use a Debian-based machine (Ubuntu, Linux Mint, Debian, etc) then use this method! APT support is hopefully coming soon. Run the following command:
::
  $ wget https://github.com/tgsachse/shellcuts/releases/download/v1.2.0/shellcuts.deb && sudo dpkg -i shellcuts.deb

**METHOD 2:** Install with wget and dnf   
RedHat-based machines (Fedora, CentOS, etc) should install using this method! DNF support is on the way. Run the following command:
::
  $ wget https://placeholder_until_I_get_the_link.rpm && sudo dnf install shellcuts.rpm

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

This syntax is disabled by default, but it can be enabled easily using this command:
::
    $ sc --enable-bashmarks-syntax

flags
-----
Here is a list of all available options/flags:

``-d, --delete [shellcut]``
  Delete the specified shellcut if it exists.
``-h, --help``
  Display a help menu for quick reference.
``-l, --list``
  List all available shellcuts.
``-n, --new [shellcut]``
  Create a new shellcut for the current working directory.
``-p, --print [shellcut]``
  Print the specified shellcut to the screen.
``--version``
  Display version information.
``--init``
  Launch the initialization script.
``--enable-bashmarks-syntax, --disable-bashmarks-syntax``
  Enable or disable Bashmarks syntax. (default: disabled)
``--enable-z, --disable-z`` (planned)
  Enable or disable z-like features. (default: disabled)
  
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
