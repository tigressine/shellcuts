#!/usr/bin/env python3
"""CLI to set up shellcuts for the first time.

This script gives users a CLI menu to help them finish setting up shellcuts.
It contains three commands:
    -Automatically modify bashrc to complete installation
    -Manually modify bashrc
    -Display contents of the script

Arguments:
    None.

Returns:
    None.

Legal:
    Author: Tiger Sachse
    License: GNU v3
    Version: 1.1.0
    Initial Release: 12/31/2017
    Current Release: 01/02/2018
"""

import os
import sys
import subprocess

# Location of bashrc and shellcuts source file.
F_BASHRC = os.expanduser('~/.bashrc')
F_SOURCE = '/usr/local/bin/shellcuts.sh'

# List of lines added to bashrc.
BASHRC_ADD = [
    "# checks if the shellcuts source file exists and includes it", 
    "if [ -f {0} ]; then".format(F_SOURCE),
    "    . {0}".format(F_SOURCE),
    "fi"]

def load_bashrc():
    """Read bashrc and returns list of lines."""
    with open(F_BASHRC, 'r') as f:
        bashrc = f.readlines()
    return bashrc

def write_bashrc(lines):
    """Write list of lines to bashrc."""
    with open(F_BASHRC, 'w') as f:
        f.writelines(lines)

# Start of main program.
subprocess.run('clear')
print("Thank you for downloading Shellcuts!\n")
print("Enter the number corresponding to the action you wish to perform:")
print("0) Automatically modify bashrc to complete installation")
print("1) Manually modify bashrc")
print("2) Display contents of this script")
command = input("> ")

if command == '0':
    """Modify bashrc file and source from modified file."""
    print("Adding to bashrc...")
    bashrc = load_bashrc()
    bashrc.append('\n')
    bashrc.extend([line+'\n' for line in BASHRC_ADD])
    write_bashrc(bashrc)
    
    print("Sourcing from bashrc...")
    subprocess.run(['.', F_BASHRC], shell=True)
    print("Done!")

elif command == '1':
    """Print necessary changes to screen for bashrc file."""
    print("Add these three lines to your .bashrc:\n")
    for line in BASHRC_ADD[1:]:
        print(line)
    print("\nNow run '. {0}' to begin using shellcuts!".format(F_BASHRC))

elif command == '2':
    """Cat this script to screen."""
    location = os.path.abspath(sys.argv[0])
    print("LOCATION: " + location)
    print("CONTENTS:")
    subprocess.run(['cat', location])
