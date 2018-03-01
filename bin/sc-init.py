"""Finishes installation of Shellcuts.

This script can automatically configure Shellcuts to be used with various
supported shells. It can also print help to allow users to do the manual
configuration.

Part of Shellcuts by Tgsachse.
"""
import re
import shutil
import subprocess
from pathlib import Path

### CONSTANTS ###
D_SHELLCUTS = Path('~/.config/shellcuts').expanduser()

INIT_SCRIPT = [
    'Thank you for installing Shellcuts.',
    '',
    'This is the initialization script to help you finish installation. If you',
    'are still seeing this prompt after automatic configuration, try restarting',
    'your terminal/reloading your shell.',
    '',
    'Listed below are your initialization options:',
    '',
    '(0)  Quit this script and do nothing. This prompt will appear again next time.',
    '(1)  Automatically configure Shellcuts for your shells. (recommended)',
    '(2)  Get help for manual configuration.',
    '(3)  Print this script to the screen.',
    '',
    'Enter the number next to the command you wish to perform: ']

MANUAL_SCRIPT = [
    'To install for {0}:',
    '',
    '(1) Copy the contents of {0}',
    '    to {0}',
    '    If the destination file does not exist then create it.',
    '',
    '(2) Copy the controller file located at {0}',
    '    to {0}',
    '',
    'That\'s it! Restart your shell session to begin using Shellcuts.']

SHELLS = {
    'bash' : {'config' : Path('~/.bashrc').expanduser(),
              'example' : Path('/usr/share/shellcuts/bash/bashrc.example'),
              'controller' : Path('/usr/share/shellcuts/bash/controller.sh')},
    'zsh' : {'config' : Path('~/.zshrc').expanduser(),
             'example' : Path('/usr/share/shellcuts/zsh/zshrc.example'),
             'controller' : Path('/usr/share/shellcuts/zsh/controller.sh')},
    'fish' : {'config' : Path('~/.config/fish/config.fish').expanduser(),
              'example' : Path('/usr/share/shellcuts/fish/config.fish.example'),
              'controller' : Path('/usr/share/shellcuts/fish/controller.fish')}}


### FUNCTIONS ###
def automatic_configuration():
    """Automatically configure Shellcuts for user.
    
    Can install for all shells or only selected shells.
    """
    shells = detect_shells()

    clear_screen()

    prompt = "Automatically configure for all shells? (yes/no): "
    yes_list = ['yes', 'y', 'Y', 'Yes']
    no_list = ['no', 'n', 'N', 'No']
    command = check_input(prompt, yes_list + no_list)
    
    selected_shells = []
    if command in yes_list:
        selected_shells = shells
    elif command in no_list:
        print_installed_shells(shells)

        print("Enter the number(s) next to the shell(s) you'd like to install Shellcuts for.")
        command = input("Separate numbers by a space: ")
        
        # Extracts numbers from user command string.
        for num in range(len(shells)):
            if re.search(str(num), command):
                selected_shells.append(shells[num])

        if len(selected_shells) == 0:
            print("No shells selected. Exiting...")
            exit(0)

    # Runs installation functions for all shells in selected_shells.
    for shell in selected_shells:
        print("Installing Shellcuts for the " + shell + " shell...")
        create_directory(D_SHELLCUTS)
        create_config(shell)
        edit_config(shell)
        install_controller(shell)

    print("\nThat's it! Restart your shell session to begin using Shellcuts.")

def check_input(prompt, acceptable_list):
    """Sanitize user input based on list of acceptable values."""
    command = input(prompt)

    tries = 0
    while command not in acceptable_list:
        tries += 1
        if tries > 5:
            print("Tries exceeded. Exiting...")
            exit(0)
        else:
            command = input("Invalid response, try again: ")

    return command

def clear_screen():
    """Clear the screen."""
    subprocess.run(['clear'])

def create_config(shell):
    """Create config file if it does not exist."""
    create_directory(SHELLS[shell]['config'].parent)
    SHELLS[shell]['config'].touch(exist_ok=True)

def create_directory(directory):
    """Create directory structure if it does not exist."""
    directory.mkdir(parents=True, exist_ok=True)

def detect_shells():
    """Return shells detected by 'which' command."""
    detected_shells = []
    
    for shell in SHELLS.keys():
        if shutil.which(shell):
            detected_shells.append(shell)
    
    return detected_shells
    
def edit_config(shell):
    """Add needed text to config file for specified shell."""
    create_config(shell)
    
    # Concatenates the example text to the config text.
    new_config = (SHELLS[shell]['config'].read_text() + '\n' +
                  SHELLS[shell]['example'].read_text())
    
    # Writes newly concatenated text to file.
    SHELLS[shell]['config'].write_text(new_config)

def exit_script():
    """Exit the script."""
    print("Exiting script...")
    exit(0)

def format_manual_script(shell):
    """Format the manual script using provided shell key."""
    formatted_script = MANUAL_SCRIPT

    # Formats lines in the MANUAL_SCRIPT based on shell.
    formatted_script[0] = formatted_script[0].format(shell)
    formatted_script[2] = formatted_script[2].format(str(SHELLS[shell]['example']))
    formatted_script[3] = formatted_script[3].format(str(SHELLS[shell]['config']))
    formatted_script[6] = formatted_script[6].format(str(SHELLS[shell]['controller']))
    formatted_script[7] = formatted_script[7].format(str(D_SHELLCUTS) + '/' + shell + '/')

    return formatted_script

def install_controller(shell):
    """Copy controller file into configuration directory."""
    destination_dir = D_SHELLCUTS.joinpath(shell)
    
    create_directory(destination_dir)

    shutil.copyfile(SHELLS[shell]['controller'],
                    destination_dir.joinpath(SHELLS[shell]['controller'].name))

def manual_configuration():
    """Show the manual configuration menus."""
    shells = detect_shells()

    clear_screen()
    
    print_installed_shells(shells)

    prompt = "Enter the number next to the shell you'd like to install: "
    acceptable_list = [str(num) for num in range(len(shells))]
    command = int(check_input(prompt, acceptable_list))

    clear_screen()

    # Formats the MANUAL_SCRIPT, then prints it line-by-line.
    formatted_manual_script = format_manual_script(shells[command])
    [print(line) for line in formatted_manual_script]

def print_installed_shells(shells):
    """Enumerate installed shells to the screen."""
    print("Currently installed shells:")

    shell_list = enumerate(shells)
    [print("{0} {1}".format(shell[0], shell[1])) for shell in shell_list]

def print_script():
    """Print the contents of this file."""
    with open(__file__) as f:
        print(f.read())

def welcome():
    """Welcome the user and present a list of options."""
    clear_screen()
    
    [print(line) for line in INIT_SCRIPT[:-1:]]

    command = check_input(INIT_SCRIPT[-1], ['0', '1', '2', '3'])

    if command == '0':
        exit_script()
    elif command == '1':
        automatic_configuration()
    elif command == '2':
        manual_configuration()
    elif command == '3':
        print_script()


### MAIN PROGRAM ###
# Try except wrapper gets rid of ugly stacktrace when using control-c to
# close the script.
try:
    welcome()
except KeyboardInterrupt:
    print()
    exit(0)
