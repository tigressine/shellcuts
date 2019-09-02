shellcuts - directory shortcuts for your shell
----------------------------------------------
Shellcuts allows you to jump between saved locations in your filesystem via a single, short command. Shellcuts can:

- create a named shellcut for any location in your filesystem
- add a follow-up command to any shellcut (like ``ls`` or ``clear``)
- save a temporary "bread crumb" shellcut
- delete any shellcut by name
- list all available shellcuts

installation
------------
Before you begin, install the latest version of `Python 3`_. You also need ``wget`` and ``tar`` to download and decompress the program initially (but if you're using Linux or MacOS you probably already have these programs installed). Execute these commands in order to install Shellcuts:
::
  cd /tmp
  wget github.com/tgsachse/shellcuts/releases/latest/download/shellcuts.tar.gz
  tar xf shellcuts.tar.gz
  cd shellcuts
  python3 install.py

usage
-----
Please see the ``man`` page for usage instructions:
::
  sc --man

.. _`Python 3`: https://www.python.org
