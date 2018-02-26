from pathlib import Path
import subprocess
import shutil

D_SHELLCUTS = Path('~/.config/shellcuts').expanduser()

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

# DONE #done
def clear_screen():
    """Clear the screen."""
    subprocess.run(['clear'])

# DONE #done
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

# DONE #DONE
def exit_script():
    """Exit the script."""
    print("Exiting script...")
    return

# DONE #DONE
def print_script():
    """Print the contents of this file."""
    with open(__file__) as f:
        print(f.read())

# DONE #DONE
def format_manual_script(shell):
    """Format the manual script using provided shell key."""
    formatted_script = MANUAL_SCRIPT

    formatted_script[0] = formatted_script[0].format(shell)
    formatted_script[2] = formatted_script[2].format(str(SHELLS[shell]['example']))
    formatted_script[3] = formatted_script[3].format(str(SHELLS[shell]['config']))
    formatted_script[6] = formatted_script[6].format(str(SHELLS[shell]['controller']))
    formatted_script[7] = formatted_script[7].format(str(D_SHELLCUTS) + '/' + shell + '/')

    return formatted_script

# DONE DONE
def manual_configuration():
    """Show the manual configuration menus."""
    shells = detect_shells()

    clear_screen()
    
    print_installed_shells()

    prompt = "Enter the number next to the shell you'd like to install: "
    command = int(check_input(prompt, [str(num) for num in range(len(shells))]))

    clear_screen()
    [print(line) for line in format_manual_script(shells[command])]

# DONE DONE
def check_input(prompt, acceptable):
    """"""
    tries = 0

    command = input(prompt)

    while command not in acceptable:
        tries += 1
        if tries > 5:
            print("Tries exceeded. Exiting...")
            exit(0)
        else:
            command = input("Invalid response, try again: ")

    return command

def print_installed_shells():
    print("Currently installed shells:")
    [print("{0} {1}".format(shell[0], shell[1])) for shell in enumerate(shells)]

def automatic_configuration():
    """"""
    shells = detect_shells()
    selected_shells = []

    clear_screen()

    command = check_output("Automatically configure for all shells? (yes/no): ",
                           ['yes', 'y', 'Y', 'Yes', 'no', 'n', 'N', 'No'])
    
    if command in ['yes', 'y', 'Y', 'Yes']:
        selected_shells = shells
    elif command in ['no', 'n', 'N', 'No']:
        print_installed_shells()
        

    [automatically_install(shell) for shell in selected_shells]

def automatically_install(shell):
    print("Installing " + shell + "...")

    create_directory(D_SHELLCUTS)
    create_shell_config(shell)
    edit_config(shell)
    install_for_shell(shell)

def confirm_shells():
    pass
    # return shells desired

# DONE #DONE
def get_output(command):
    """Run command and return output."""
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    
    return process.communicate()[0].decode('UTF-8')

# DONE #DONE
def detect_shells():
    """Return shells detected by 'which' command."""
    detected_shells = []
    
    for shell in SHELLS.keys():
        if get_output(['which', shell]):
            detected_shells.append(shell)
    
    return detected_shells

# DONE #DONE --weird write protected message when deleting
def install_for_shell(shell):
    destination_dir = Path(str(D_SHELLCUTS) + '/' + shell)
    create_directory(destination)

    shutil.copy(SHELLS[shell]['controller'], destination)

# DONE #DONE
def edit_config(shell):
    """Add needed text to config file for specified shell."""
    create_shell_config(shell)
    
    new_config = (SHELLS[shell]['config'].read_text() + '\n' +
                  SHELLS[shell]['example'].read_text())
    
    SHELLS[shell]['config'].write_text(new_config)

# DONE #DONE
def create_shell_config(shell):
    """Create config file if it does not exist."""
    SHELLS[shell]['config'].parent.mkdir(parents=True, exist_ok=True)
    SHELLS[shell]['config'].touch(exist_ok=True)

# DONE #DONE
def create_directory(directory):
    """Create directory structure if it does not exist."""
    directory.mkdir(parents=True, exist_ok=True)

welcome()
