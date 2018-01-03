shellcuts - directory shortcuts for your shell
----------------------------------------------

Shellcuts allow you to save locations in your file system and jump to those locations later with a simple command (like bookmarks). This program aims to include what other, similar programs are missing, and acts as a drop-in replacement for Bashmarks_ and `other-shell derivatives`_. Features include:

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
- installable via Apt, Homebrew
- possibly include z-like_ functionality

.. _Bashmarks: https://www.github.com/huyng/bashmarks
.. _`other-shell derivatives`: https://github.com/search?utf8=%E2%9C%93&q=bashmarks&type=
.. _z-like: https://github.com/rupa/z

installation
------------

Shellcuts is meant to be easy to install. Use any of the following methods to install Shellcuts. Since this program is written in `Python 3`_, you need the latest version installed for it to work!

**METHOD 1:** Install with Pip_

If you have pip3 installed, run this command to install shellcuts:
::
  $ sudo pip3 install shellcuts

**METHOD 2:** Install with Apt (PLANNED)

If you are running a Linux distribution that uses Apt to manage packages (e.g. Ubuntu, Kubuntu, Debian), run this command to install shellcuts:
::
  $ sudo apt install shellcuts
  
**METHOD 3:** Install with Homebrew (PLANNED)

If you're on Mac and have Homebrew installed, run this command to install shellcuts:
::
  $ brew install shellcuts

.. _`Python 3`: https://www.python.org
.. _Pip: https://pip.pypa.io/en/stable/
.. _`distribution's software repositories`: https://docs.aws.amazon.com/cli/latest/userguide/awscli-install-linux-python.html
