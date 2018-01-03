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
- installable via Pip_ (change this link to link to project page)

Planned features include:

- tab completion
- Fish, Zsh, Csh, Korn shell support
- installable via Apt, Homebrew
- possibly include z-like_ functionality

.. _Bashmarks: https://www.github.com/huyng/bashmarks
.. _`other-shell derivatives`: https://github.com/search?utf8=%E2%9C%93&q=bashmarks&type=
.. _Pip: https://pypi.python.org/pypi
.. _z-like: https://github.com/rupa/z

installation
------------

Shellcuts is meant to be easy to install, as well as easy to use. To provide choices to the user I've included many methods to install. Choose any of these options to install, they all result in the same thing.

**Install Python 3**

NOTE: Because this program is written in `Python 3.6`_, you will need the latest version of Python installed on your system. To check if Python is already installed (as is typically the case with modern Linux distributions) run this command:
::
  $ python3 --version
If this code outputs something like 'Python 3.X.X' then you're all set! If it results in an error or says Python3 is not installed, follow `this link`_, download the latest build, and install or install through your `distribution's software repositories`_.

| **Install Shellcuts**   
| OPTION 1: Pip Installation

First, make sure you have the Python 3 version of Pip (pip3). To check, run:
::
  $ pip3 --version
If the output is an error, you must install pip3. Do this through your distribution's software repositories. For example, on Ubuntu run:
::
  $ sudo apt install python3-pip
If you are using a different distribution, like Fedora, CentOS, Arch, etc., then do a quick Google search and figure out how to install for your distribution. :) Once pip3 is installed, run this command to install shellcuts:
::
  $ sudo pip3 install shellcuts

OPTION 2: Apt installation

This method only works if you are running Ubuntu or a Debian distribution that uses Apt to manage it's packages. Run this command:
::
  $ sudo apt install shellcuts
  
OPTION 3: Homebrew installation

.. _`Python 3.6`:
.. _`this link`: https://www.python.org
.. _`distribution's software repositories`: https://docs.aws.amazon.com/cli/latest/userguide/awscli-install-linux-python.html
