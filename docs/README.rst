shellcuts - directory shortcuts for your shell
----------------------------------------------

Shellcuts  are  directory shortcuts for your shell. This program allows you to save locations in 
your filesystem and then cut back to those locations with a single, short command. This  program
is  inspired  by  Bashmarks  and  hopes  to  improve on Bashmarks by supporting more systems and
shells. Shellcuts includes the following features:

- creates named shellcuts to any location in the filesystem
- lists all saved shellcuts
- deletes shellcuts by name
- saves shellcuts on a per-user basis
- Bashmarks syntax is supported for user comfort and familiarity
- supports Bash, Fish, Ksh, and Zsh

Planned features include:

- tab completion
- easy compatibility with competing software

installation
------------

Shellcuts is easy to install and doesn't require any special privileges! To run, you need the latest version of `Python 3`_ installed, as well as a supported shell. Linux users almost certainly have both of these but macOS users may need to install Python3. Shellcuts is not available for Windows shell or PowerShell.

**METHOD 1:** Install with ``wget`` and ``tar``

The following commands will work for nearly everyone. If it does not work for you, try the next method.
::
  cd /tmp && wget https://github.com/tgsachse/shellcuts/archive/v1.2.3.tar.gz
  tar -xzf v1.2.3.tar.gz && cd shellcuts-1.2.3
  python3 install.py

**METHOD 2:** Install with ``git``

This method requires that you have ``git`` installed on your machine. Run these commands:
::
  cd /tmp && git clone https://www.github.com/tgsachse/shellcuts.git
  cd shellcuts && python3 install.py

**METHOD 3:** Install manually

Download Shellcuts from `this link`_ and unzip it using ``tar`` or any other decompression software. Next, navigate into the decompressed files and run the ``install.py`` script using this command:
::
  python3 install.py

usage
-----
The core command for Shellcuts is ``sc`` and this program includes the following aliases:

- ``scut``
- ``shellc``
- ``shellcut``
- ``shellcuts``

Feel free to use any of the above or the main ``sc`` command to operate Shellcuts. This program also includes aliases to replicate Bashmarks_ syntax. They are as follows:

- ``g`` to go, equivalent to ``sc``
- ``s`` to save, equivalent to ``sc -n``
- ``d`` to delete, equivalent to ``sc -d``
- ``p`` to print, equivalent to ``sc -p``
- ``l`` to list, equivalent to ``sc -l``

flags
-----
Here is a list of all available options/flags:

``-n, --new [shellcut] {follow}``
  Create a new shellcut for the current directory with an optional follow up command.
``-m, --move [shellcut]``
  Move an existing shellcut to a new directory.
``-d, --delete [shellcut]``
  Delete the specified shellcut if it exists.
``-p, --print [shellcut]``
  Print the specified shellcut to the screen.
``-f, --follow [shellcut] [follow]``
  Add a follow up command that executes after each jump to a particular shellcut.
``-l, --list``
  List all available shellcuts.
``-c, --crumb``
  Create a temporary bread crumb that can be jumped to via ``sc`` alone.
``-h, --help``
  Display a help menu for quick reference.
``--unfollow [shellcut]``
  Remove a follow up command from a particular shellcut.
``--version``
  Display version information.
``--man``
  Display a Linux manual page.
  
examples
--------
Here are some examples of Shellcuts in action. See this program's manual page for more.
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
.. _`Python 3`: https://www.python.org
.. _`this link`: https://github.com/tgsachse/shellcuts/archive/v1.2.3.tar.gz
