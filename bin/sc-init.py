"""
"""
import re
import shutil
import subprocess
from pathlib import Path

### CONSTANTS ###
D_CONFIG = Path('~/.config/shellcuts').expanduser()
SHELL_DATA = {
    'bash': {'share' : Path('/usr/share/shellcuts/bash'),
             'config' : Path('~/.bashrc').expanduser(),
             'exclude' : ('bashrc.example',
                          'bashmarks-aliases.sh')},
                          
    'zsh': {'share' : Path('/usr/share/shellcuts/zsh'),
            'config' : Path('~/.zshrc').expanduser(),
            'exclude' : ('zshrc.example',
                         'bashmarks-aliases.sh')},

    'fish': {'share' : Path('/usr/share/shellcuts/fish'),
             'config' : Path('~/.config/fish/config.fish').expanduser(),
             'exclude' : ('config.fish.example',
                          'bashmarks-aliases.fish')}
}


### FUNCTIONS ###
def check_home_config_dir():
    """"""
    D_CONFIG.mkdir(parents=True, exist_ok=True)

def check_shell_config(shell):
    """"""
    SHELL_DATA[shell]['config'].touch(exist_ok=True)

def install_share_files(shell):
    """"""
    check_home_config_dir()

    if (D_CONFIG / shell).is_dir():
        shutil.rmtree(str(D_CONFIG / shell))
        
    shutil.copytree(str(SHELL_DATA[shell]['share']),
                    str(D_CONFIG / shell),
                    ignore=shutil.ignore_patterns(*SHELL_DATA[shell]['exclude']))

def modify_shell_config(shell):
    """"""
    check_shell_config(shell)

    F_CONFIG = SHELL_DATA[shell]['share'] / SHELL_DATA[shell]['exclude'][0]
    new_config_text =  (SHELL_DATA[shell]['config'].read_text() + 
                        '\n' +
                        F_CONFIG.read_text())
    SHELL_DATA[shell]['config'].write_text(new_config_text)


### SCREEN ###
def get_output(command):
    """"""
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    return process.communicate()[0].decode('UTF-8')

def detect_shells():
    """"""
    shells = []
    for shell in SHELL_DATA.keys():
        if get_output(['which', shell]):
            shells.append(shell)

    return shells

def automatic_configuration():
    shells = detect_shells()

    subprocess.run(['clear'])
    print("youve got these shells:")
    for i, shell in enumerate(shells):
        print("({0})  {1}".format(i, shell))

    print("Enter the number(s) of the shell(s) you want to automatically configure Shellcuts for")
    print("To cancel, press 'q'")
    numbers = input(": ")
    range_ = '[q0-{}]'.format(len(shells) - 1)
    numz = set(re.findall(range_, str(numbers)))
    #print(numz)
    if 'q' in numz:
        print('quitting')
        exit(0)



INIT = [
    'Thank you for installing Shellcuts.',
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

def main():
    format2 = '{:^80}'
    formatt = '{:80}'

    subprocess.run(['clear'])
    print(format2.format(INIT[0]))
    print(format2.format(''))
    [print(formatt.format(line)) for line in INIT[1:-1:]]

    command = input(INIT[-1])
    while command not in ['0','1','2','3']:
        command = input('Invalid command, try again: ')

    if command == '0':
        exit(0)
    elif command == '1':
        automatic_configuration()
    elif command == '2':
        manual_configuration()
    elif command == '3':
        print_script()

if __name__ == '__main__':
    main()