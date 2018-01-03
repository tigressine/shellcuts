shellcuts - directory shortcuts for your shell
----------------------------------------------

Shellcuts allow you to save locations in your filesystem and jump to those locations later with a simple command (much like bookmarks). This program aims to include what other, similar programs are missing, and acts as a drop-in replacement for Bashmarks_ and `other-shell derivatives`_. Shellcuts includes the following features:

- creates named shellcuts to any location in the filesystem
- lists all saved shellcuts
- deletes shellcuts by name
- saves shellcuts on a per-user basis
- supports Bashmarks syntax for user comfort and familiarity
- written mostly in Python for portability
- supports Bash shell
- installable via Pip

Planned features include:

- tab completion
- Fish, Zsh, Csh, Korn shell support
- installable via APT, Homebrew
- possibly include z-like_ functionality

installation
------------

Shellcuts is meant to be easy to install--use any of the following methods. You need the latest version of `Python 3`_ installed for it to work!

**METHOD 1:** Install with Pip_

If you have pip3 installed, run this command to install Shellcuts:
::
  $ sudo pip3 install shellcuts

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
When you first install Shellcuts, you must run the program initialization script once to finish configuration. Simply run this command to launch the configuration utility:
::
  $ sc-init
The configuration utility will give you the option to automatically configure your system to use Shellcuts, or it will tell you how to do the configuration manually. I highly recommend using the automatic configuration, as it's not prone to human error and is designed to make setup super easy!

The core command for Shellcuts is ``sc``. By default, Shellcuts includes these aliases for ``sc``:

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

NEW: ``-n, --new [name]``
  Add a shellcut for the current working directory, named *name*.
DELETE: ``-d, --delete [name]``
  Delete shellcut named *name* if it exists.
PRINT: ``-p, --print [name]``
  Print the location saved by the shellcut named *name*.
LIST: ``-l, --list``
  List all available shellcuts.
(planned) VERSION: ``-v, --version``
  Get Shellcuts version information.
(planned) Z SETTINGS: ``--enable-z, --disable-z``
  Enable or disable z-like features.
(planned) REINITIALIZE: ``--init``
  Rerun the initial setup script.
(planned) HELP: ``-h, --help``
  Launch a help menu.
  
examples
--------
Here are some examples of Shellcuts in action.
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
.. _`other-shell derivatives`: https://github.com/search?utf8=%E2%9C%93&q=bashmarks&type=
.. _z-like: https://github.com/rupa/z
.. _`Python 3`: https://www.python.org
.. _Pip: https://pip.pypa.io/en/stable/
.. _APT: https://en.wikipedia.org/wiki/APT_(Debian)
.. _Homebrew: https://brew.sh/
.. _Git: https://git-scm.com
