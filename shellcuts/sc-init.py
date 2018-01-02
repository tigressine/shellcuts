#!/usr/bin/env python3
import os
import sys
import subprocess

def load_bashrc():
    with open(F_BASHRC, 'r') as f:
        bashrc = f.readlines()
    return bashrc

def write_bashrc(lines):
    with open(F_BASHRC, 'w') as f:
        for line in lines:
            f.write(line)

F_BASHRC = 'bashrc.txt'#os.expanduser('~/.bashrc')
F_SOURCE = "/usr/local/bin/shellcuts.sh"

subprocess.run('clear')
print("Thank you for downloading Shellcuts!\n")
print("Enter the number corresponding to the action you wish to perform:")
print("0) Automatically modify bashrc to complete installation")
print("1) Manually modify bashrc")
print("2) Display contents of this script")
command = input("> ")

if command == '0':
    print("Adding to bashrc...")
    bashrc = load_bashrc()
    bashrc.append("\n")
    bashrc.append("# checks if the shellcuts source file exists and includes it\n")
    bashrc.append("if [ -f {0} ]; then\n".format(F_SOURCE))
    bashrc.append("    source {0}\n".format(F_SOURCE))
    bashrc.append("fi")

    print(bashrc)
    write_bashrc(bashrc)
    print("Sourcing from bashrc...")
    #subprocess.run(['source', F_BASHRC])

    print("Done!")

elif command == '1':
    pass

elif command == '2':
    print("LOCATION: " + os.path.abspath(sys.argv[0]))
    print("\nCONTENTS:\n")
    subprocess.run(['cat', sys.argv[0][2:]])#
